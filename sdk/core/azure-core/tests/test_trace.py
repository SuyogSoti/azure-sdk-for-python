import unittest
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


class MockClient:
    @use_distributed_traces
    def __init__(self, policies=None):
        self.request = HttpRequest("GET", "https://bing.com")
        if policies is None:
            policies = []
        policies.append(mock.Mock(spec=HTTPPolicy, send=self.verify_request))
        self.policies = policies
        self.transport = mock.Mock(spec=HttpTransport)
        self.pipeline = Pipeline(self.transport, policies=policies)

        self.expected_response = mock.Mock(spec=PipelineResponse)

    @use_distributed_traces
    def verify_request(self, request):
        current_span = tracing_context.get_current_span()
        header = current_span.to_header()
        if len(self.policies) > 1 and current_span is not None:
            dist_pol = self.policies[0]
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


class ModelOpencensusSpan:
    def __init__(self, name):
        self.name = name
        self.span_id = 0
        self.children = []
        self.attrs = {}
        self.annotations = []
        self.start_time = None
        self.end_time = None
        self.context_tracer = None

    def span(self, name="child_span"):
        child = ModelOpencensusSpan(name)
        self.children.append(child)
        return child

    def add_attribute(self, attribute_key, attribute_value):
        self.attrs[attribute_key] = attribute_value

    def add_annotation(self, description, **attrs):
        self.annotations.append(description)

    def start(self):
        self.start_time = 0

    def finish(self):
        self.end_time = 1


class ModelDataDogSpan:
    def __init__(self, name):
        self.name = name
        self.span_id = 0
        self.attrs = {}
        self.annotations = []
        self.children = []
        self.start_time = None
        self.end_time = None
        self.start = 0
        self.trace_id = 0

    class Tracer:
        def start_span(self, name="", child_of=None):
            child = ModelDataDogSpan(name)
            if child_of is not None:
                child_of.children.append(child)
            return child

    def tracer(self):
        return self.Tracer()

    def set_tag(self, attribute_key, attribute_value):
        self.attrs[attribute_key] = attribute_value

    def finish(self):
        self.end_time = 1


class TestUseDistributedTraces(unittest.TestCase):
    def test_use_distributed_traces_decorator(self):
        client = MockClient(policies=[])
        parent = ModelOpencensusSpan("Overall")
        client.get_foo(parent_span=parent, tracer="opencensus")
        assert parent.children[0].name == "MockClient.get_foo()"
        assert len(parent.children[0].children) == 0

    def test_with_parent_span_with_opencensus(self):
        client = MockClient(policies=[DistributedTracer()])
        parent = ModelOpencensusSpan("Overall")
        attrs = {"firstKey": "firstVal", "secondKey": "secondVal"}
        annotations = ["first Ann", "Second Ann"]
        client.make_request(
            2, parent_span=parent, tracer="opencensus"
        )
        assert len(parent.children[0].children) == 2
        span = parent.children[0].children[0]
        # TODO(suyogsoti)figure out a way to add annotations
        # assert attrs == span.attrs
        # assert annotations == span.annotations

    def test_with_parent_span_with_datadog(self):
        client = MockClient(policies=[DistributedTracer()])
        parent = ModelDataDogSpan("Overall")
        attrs = {"firstKey": "firstVal", "secondKey": "secondVal"}
        client.make_request(2, parent_span=parent, tracer="datadog")
        assert len(parent.children[0].children) == 2
        # TODO(suyogsoti)figure out a way to add annotations

    def test_without_parent_span_with_tracing_policies(self):
        client = MockClient(policies=[DistributedTracer()])
        res = client.make_request(2)
        assert res is client.expected_response

    def test_with_parent_span_without_tracing_policies(self):
        client = MockClient(policies=[])
        parent = ModelOpencensusSpan("Overall")
        client.make_request(2, parent_span=parent)
        assert len(parent.children[0].children) == 1

    def test_without_parent_span_without_tracing_policies(self):
        client = MockClient(policies=[])
        res = client.make_request(2)
        assert res is client.expected_response


if __name__ == "__main__":
    unittest.main()
