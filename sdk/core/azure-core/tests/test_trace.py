import unittest
import pytest

try:
    from unittest import mock
except ImportError:
    import mock
from azure.core import HttpRequest
from azure.core.pipeline import Pipeline, PipelineResponse
from azure.core.pipeline.policies import HTTPPolicy
from azure.core.pipeline.policies.distributed_tracing import DistributedTracer
from azure.core.pipeline.transport import HttpTransport
from azure.core.trace import use_distributed_traces
from azure.core.trace.context import tracing_context
from azure.core.trace.span import DataDogSpan
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
        current_span = tracing_context.get_current_span()
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

    @use_distributed_traces
    def make_request(self, numb_times, **kwargs):
        if numb_times < 1:
            return None
        response = self.pipeline.run(self.request, **kwargs)
        self.get_foo()
        self.make_request(numb_times - 1, **kwargs)
        return response

    @use_distributed_traces
    def get_foo(self):
        return 5


class TestUseDistributedTraces(unittest.TestCase):
    def test_use_distributed_traces_decorator(self):
        client = MockClient(policies=[])
        parent = Span(name="Overall")
        client.get_foo(parent_span=parent, tracer="opencensus")
        client.get_foo(parent_span=parent)
        assert len(parent.children) == 2
        assert not parent.children[1].children
        assert parent.children[0].name == "MockClient.get_foo"
        assert not parent.children[0].children
        parent.finish()

    def test_parent_span_with_opencensus(self):
        trace = tracer.Tracer(sampler=AlwaysOnSampler())
        parent = trace.start_span(name="OverAll")
        client = MockClient(policies=[DistributedTracer()])
        attrs = {"firstKey": "firstVal", "secondKey": "secondVal"}
        annotations = ["first Ann", "Second Ann"]
        client.make_request(2)
        client.make_request(2, tracer="opencensus")
        client.make_request(2)
        client.make_request(2, parent_span=parent, tracer="opencensus")
        client.make_request(2)
        client.make_request(2, tracer="opencensus")
        client.make_request(2)
        assert len(parent.children) == 3
        assert parent.children[0].name == "MockClient.make_request"
        children = parent.children[0].children
        assert len(children) == 3
        # TODO(suyogsoti)figure out a way to add annotations
        # span = parent.children[0].children[0]
        # assert attrs == span.attrs
        # assert annotations == span.annotations
        parent.finish()
        trace.end_span()

    def get_children_of_datadog_span(self, parent, tracer):
        traces = tracer.context_provider._local._locals.context._trace
        return [x for x in traces if x.parent_id == parent.span_id]

    @pytest.mark.skip(
        "Datadog isssue: https://github.com/DataDog/dd-trace-py/issues/968"
    )
    def test_with_parent_span_with_datadog(self):
        client = MockClient(policies=[DistributedTracer()])
        parent = dd_tracer.trace(
            name="Overall", service="suyog-azure-core-v0.01-datadog"
        )
        attrs = {"firstKey": "firstVal", "secondKey": "secondVal"}
        client.make_request(2)
        client.make_request(2, tracer="datadog")
        client.make_request(2)
        chlds = self.get_children_of_datadog_span(parent, dd_tracer)
        assert len(chlds) == 1
        client.make_request(2, parent_span=parent, tracer="datadog")
        client.make_request(2)
        chlds = self.get_children_of_datadog_span(parent, dd_tracer)
        assert len(chlds) == 2
        client.make_request(2, tracer="datadog")
        client.make_request(2)
        chlds = self.get_children_of_datadog_span(parent, dd_tracer)
        assert len(chlds) == 3
        assert chlds[0].name == "MockClient.make_request"
        assert chlds[1].name == "MockClient.make_request"
        assert chlds[2].name == "MockClient.make_request"
        grandChlds = self.get_children_of_datadog_span(chlds[0], dd_tracer)
        assert len(grandChlds) == 3
        grandChlds = self.get_children_of_datadog_span(chlds[1], dd_tracer)
        assert len(grandChlds) == 3
        # TODO(suyogsoti)figure out a way to add annotations
        parent.finish()

    def test_trace_with_not_setup(self):
        with pytest.raises(AssertionError):
            client = MockClient(
                policies=[DistributedTracer()], assert_current_span=True
            )
            client.make_request(2)
        os_env = mock.patch.dict(
            os.environ, {"azure_sdk_for_python_tracer": "opencensus"}
        )
        os_env.start()
        client = MockClient(policies=[DistributedTracer()], assert_current_span=True)
        client.make_request(2)
        os_env.stop()

    def test_blacklist_works(self):
        trace = tracer.Tracer(sampler=AlwaysOnSampler())
        parent = trace.start_span(name="OverAll")
        client = MockClient(policies=[DistributedTracer()])
        client.make_request(2, tracer="opencensus")
        assert len(parent.children) == 1
        client.make_request(2, tracer="opencensus", blacklist=["make_request"])
        assert len(parent.children) == 5
        parent.finish()
        trace.end_span()

    def test_without_parent_span_with_tracing_policies(self):
        client = MockClient(policies=[DistributedTracer()])
        res = client.make_request(2)
        assert res is client.expected_response

    def test_with_parent_span_without_tracing_policies(self):
        client = MockClient(policies=[])
        parent = Span(name="Overall")
        client.make_request(2, parent_span=parent)
        assert len(parent.children[0].children) == 2
        parent.finish()

    def test_without_parent_span_without_tracing_policies(self):
        client = MockClient(policies=[])
        res = client.make_request(2)
        assert res is client.expected_response


if __name__ == "__main__":
    unittest.main()
