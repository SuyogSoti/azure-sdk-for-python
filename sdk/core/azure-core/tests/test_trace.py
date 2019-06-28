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
from azure.core.trace import use_distributed_traces
from azure.core.trace.context import tracing_context
from azure.core.settings import settings
from opencensus.trace import config_integration
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
            header_label = ""
            impl_lib = settings.tracing_implementation()
            if impl_lib is "opencensus":
                header_label = "traceparent"
            elif impl_lib is "datadog":
                header_label = "x-datadog-trace-id"
            assert header_label in request.http_request.headers
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


class TestTrace(unittest.TestCase):
    def test_use_distributed_traces_decorator(self):
        settings.tracing_implementation.set_value("opencensus")
        trace = tracer.Tracer(sampler=AlwaysOnSampler())
        parent = trace.start_span(name="OverAll")
        client = MockClient(policies=[])
        client.get_foo(parent_span=parent)
        client.get_foo()
        assert len(parent.children) == 3
        assert parent.children[0].name == "MockClient.__init__"
        assert not parent.children[0].children
        assert parent.children[1].name == "MockClient.get_foo"
        assert not parent.children[1].children
        parent.finish()
        trace.finish()
        settings.tracing_implementation.unset_value()

    def test_parent_span_with_opencensus(self):
        settings.tracing_implementation.set_value("opencensus")
        trace = tracer.Tracer(sampler=AlwaysOnSampler())
        parent = trace.start_span(name="OverAll")
        client = MockClient(policies=[DistributedTracer()])
        client.make_request(2)
        with parent.span("child") as child:
            client.make_request(2, parent_span=child)
        client.make_request(2)
        assert len(parent.children) == 4
        assert parent.children[0].name == "MockClient.__init__"
        assert parent.children[1].name == "MockClient.make_request"
        assert parent.children[2].children[0].name == "MockClient.make_request"
        children = parent.children[1].children
        assert len(children) == 3
        parent.finish()
        trace.end_span()
        settings.tracing_implementation.unset_value()

    def get_children_of_datadog_span(self, parent, tracer):
        traces = tracer.context_provider._local._locals.context._trace
        return [x for x in traces if x.parent_id == parent.span_id]

    def test_with_parent_span_with_datadog(self):
        settings.tracing_implementation.set_value("datadog")
        parent = dd_tracer.trace(
            name="Overall", service="suyog-azure-core-v0.01-datadog"
        )
        client = MockClient(policies=[DistributedTracer()])
        chlds = self.get_children_of_datadog_span(parent, dd_tracer)
        assert len(chlds) == 1
        client.make_request(2)
        chlds = self.get_children_of_datadog_span(parent, dd_tracer)
        assert len(chlds) == 2
        client.make_request(2, parent_span=parent)
        chlds = self.get_children_of_datadog_span(parent, dd_tracer)
        assert len(chlds) == 3
        client.make_request(2)
        chlds = self.get_children_of_datadog_span(parent, dd_tracer)
        assert len(chlds) == 4
        assert chlds[0].name == "MockClient.__init__"
        assert chlds[1].name == "MockClient.make_request"
        assert chlds[2].name == "MockClient.make_request"
        assert chlds[3].name == "MockClient.make_request"
        grandChlds = self.get_children_of_datadog_span(chlds[1], dd_tracer)
        assert len(grandChlds) == 3
        grandChlds = self.get_children_of_datadog_span(chlds[2], dd_tracer)
        assert len(grandChlds) == 3
        parent.finish()
        settings.tracing_implementation.unset_value()

    def test_trace_with_no_setup(self):
        with pytest.raises(AssertionError):
            client = MockClient(
                policies=[DistributedTracer()], assert_current_span=True
            )
            client.make_request(2)
        os_env = mock.patch.dict(
            os.environ, {"AZURE_SDK_TRACING_IMPLEMENTATION": "opencensus"}
        )
        os_env.start()
        client = MockClient(policies=[DistributedTracer()], assert_current_span=True)
        client.make_request(2)
        os_env.stop()

    def test_without_parent_span_with_tracing_policies(self):
        settings.tracing_implementation.unset_value()
        client = MockClient(policies=[DistributedTracer()])
        res = client.make_request(2)
        assert res is client.expected_response

    def test_with_parent_span_without_tracing_policies(self):
        client = MockClient(policies=[])
        parent = Span(name="Overall")
        client.make_request(2, parent_span=parent)
        assert len(parent.children[0].children) == 3
        parent.finish()

    def test_without_parent_span_without_tracing_policies(self):
        client = MockClient(policies=[])
        res = client.make_request(2)
        assert res is client.expected_response

    def test_multi_threaded_work(self):
        config_integration.trace_integrations(["threading"])
        settings.tracing_implementation.set_value("opencensus")
        trace = tracer.Tracer(sampler=AlwaysOnSampler())
        parent = trace.start_span(name="OverAll")
        client = MockClient(policies=[DistributedTracer()])

        threads = []
        number_of_threads = 4
        for i in range(number_of_threads):
            th = threading.Thread(
                target=tracing_context.with_current_context(client.make_request),
                args=(3,),
            )
            threads.append(th)
            th.start()

        for thread in threads:
            thread.join()

        client.make_request(3)

        assert len(parent.children) == number_of_threads + 2
        parent.finish()
        trace.end_span()
        settings.tracing_implementation.unset_value()


if __name__ == "__main__":
    unittest.main()
