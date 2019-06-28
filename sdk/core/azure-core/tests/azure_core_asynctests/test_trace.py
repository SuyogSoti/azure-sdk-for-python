import unittest
import pytest
import threading

try:
    from unittest import mock
except ImportError:
    import mock
from azure.core import HttpRequest
from azure.core.pipeline import Pipeline, PipelineResponse
from azure.core.pipeline.policies import HTTPPolicy
from azure.core.pipeline.policies.distributed_tracing import DistributedTracer
from azure.core.pipeline.transport import HttpTransport
from azure.core.trace import use_distributed_traces, use_distributed_traces_async
from azure.core.trace.context import tracing_context
from azure.core.settings import settings
import os


from opencensus.trace import tracer, Span
from opencensus.trace.samplers import AlwaysOnSampler
from ddtrace import tracer as dd_tracer


class MockClient:
    @use_distributed_traces
    def __init__(self, policies=None, assert_current_span=False):
        self.request = HttpRequest("GET", "https://bing.com")
        if policies is None:
            policies = []
        policies.append(mock.Mock(spec=HTTPPolicy, send=self.verify_request))
        self.policies = policies
        self.transport = mock.Mock(spec=HttpTransport)
        self.pipeline = Pipeline(self.transport, policies=policies)

        self.expected_response = mock.Mock(spec=PipelineResponse)
        self.assert_current_span = assert_current_span

    def verify_request(self, request):
        current_span = tracing_context.current_span.get()
        if self.assert_current_span:
            assert current_span is not None
        if (
            len(self.policies) > 1
            and current_span is not None
            and len(current_span.children) > 0
        ):
            header = current_span.children[0].to_header({})
            dist_pol = self.policies[0]
            header_label = ""
            if current_span.impl_library is "opencensus":
                header_label = "traceparent"
            elif current_span.impl_library is "datadog":
                header_label = "x-datadog-trace-id"
            assert header_label in request.http_request.headers
            assert request.http_request.headers[dist_pol.header_label] == header
        return self.expected_response

    @use_distributed_traces_async
    async def make_request(self, numb_times, **kwargs):
        if numb_times < 1:
            return None
        response = self.pipeline.run(self.request, **kwargs)
        await self.get_foo()
        await self.make_request(numb_times - 1, **kwargs)
        return response

    @use_distributed_traces_async
    async def get_foo(self):
        return 5


@pytest.mark.asyncio
async def test_use_distributed_traces_decorator():
    os_env = mock.patch.dict(
        os.environ, {"AZURE_SDK_TRACING_IMPLEMENTATION": "opencensus"}
    )
    os_env.start()
    trace = tracer.Tracer(sampler=AlwaysOnSampler())
    parent = trace.start_span(name="OverAll")
    client = MockClient(policies=[])
    await client.get_foo(parent_span=parent)
    await client.get_foo()
    assert len(parent.children) == 3
    assert parent.children[0].name == "MockClient.__init__"
    assert not parent.children[0].children
    assert parent.children[1].name == "MockClient.get_foo"
    assert not parent.children[1].children
    parent.finish()
    trace.finish()
    os_env.stop()


@pytest.mark.asyncio
async def test_parent_span_with_opencensus():
    os_env = mock.patch.dict(
        os.environ, {"AZURE_SDK_TRACING_IMPLEMENTATION": "opencensus"}
    )
    os_env.start()
    trace = tracer.Tracer(sampler=AlwaysOnSampler())
    parent = trace.start_span(name="OverAll")
    client = MockClient(policies=[DistributedTracer()])
    await client.make_request(2)
    with parent.span("child") as child:
        await client.make_request(2, parent_span=child)
    await client.make_request(2)
    assert len(parent.children) == 4
    assert parent.children[0].name == "MockClient.__init__"
    assert parent.children[1].name == "MockClient.make_request"
    assert parent.children[2].children[0].name == "MockClient.make_request"
    children = parent.children[1].children
    assert len(children) == 3
    parent.finish()
    trace.end_span()
    os_env.stop()


def get_children_of_datadog_span(parent, tracer):
    traces = tracer.context_provider._local._locals.context._trace
    return [x for x in traces if x.parent_id == parent.span_id]


@pytest.mark.asyncio
async def test_with_parent_span_with_datadog():
    os_env = mock.patch.dict(
        os.environ, {"AZURE_SDK_TRACING_IMPLEMENTATION": "datadog"}
    )
    os_env.start()
    parent = dd_tracer.trace(name="Overall", service="suyog-azure-core-v0.01-datadog")
    client = MockClient(policies=[DistributedTracer()])
    chlds = get_children_of_datadog_span(parent, dd_tracer)
    assert len(chlds) == 1
    await client.make_request(2)
    chlds = get_children_of_datadog_span(parent, dd_tracer)
    assert len(chlds) == 2
    await client.make_request(2, parent_span=parent)
    chlds = get_children_of_datadog_span(parent, dd_tracer)
    assert len(chlds) == 3
    await client.make_request(2)
    chlds = get_children_of_datadog_span(parent, dd_tracer)
    assert len(chlds) == 4
    assert chlds[0].name == "MockClient.__init__"
    assert chlds[1].name == "MockClient.make_request"
    assert chlds[2].name == "MockClient.make_request"
    assert chlds[3].name == "MockClient.make_request"
    grandChlds = get_children_of_datadog_span(chlds[1], dd_tracer)
    assert len(grandChlds) == 3
    grandChlds = get_children_of_datadog_span(chlds[2], dd_tracer)
    assert len(grandChlds) == 3
    parent.finish()
    os_env.stop()


@pytest.mark.asyncio
async def test_trace_with_no_setup():
    with pytest.raises(AssertionError):
        client = MockClient(policies=[DistributedTracer()], assert_current_span=True)
        await client.make_request(2)
    os_env = mock.patch.dict(
        os.environ, {"AZURE_SDK_TRACING_IMPLEMENTATION": "opencensus"}
    )
    os_env.start()
    client = MockClient(policies=[DistributedTracer()], assert_current_span=True)
    await client.make_request(2)
    os_env.stop()


@pytest.mark.asyncio
async def test_without_parent_span_with_tracing_policies():
    client = MockClient(policies=[DistributedTracer()])
    res = await client.make_request(2)
    assert res is client.expected_response


@pytest.mark.asyncio
async def test_with_parent_span_without_tracing_policies():
    client = MockClient(policies=[])
    parent = Span(name="Overall")
    await client.make_request(2, parent_span=parent)
    assert len(parent.children[0].children) == 3
    parent.finish()


@pytest.mark.asyncio
async def test_without_parent_span_without_tracing_policies():
    client = MockClient(policies=[])
    res = await client.make_request(2)
    assert res is client.expected_response


if __name__ == "__main__":
    unittest.main()
