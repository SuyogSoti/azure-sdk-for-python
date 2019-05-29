# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# --------------------------------------------------------------------------

import json
import unittest

import requests

try:
    from unittest import mock
except ImportError:
    import mock
import xml.etree.ElementTree as ET
import sys

import pytest

from azure.core.pipeline import Pipeline, use_distributed_traces, PipelineResponse
from azure.core.pipeline.policies import (
    SansIOHTTPPolicy,
    UserAgentPolicy,
    RedirectPolicy,
    HTTPPolicy,
)
from azure.core.pipeline.policies.distributed_tracing import DistributedTracer
from azure.core.pipeline.transport import HttpRequest, HttpTransport, RequestsTransport

from azure.core.configuration import Configuration


def test_sans_io_exception():
    class BrokenSender(HttpTransport):
        def send(self, request, **config):
            raise ValueError("Broken")

        def open(self):
            self.session = requests.Session()

        def close(self):
            self.session.close()

        def __exit__(self, exc_type, exc_value, traceback):
            """Raise any exception triggered within the runtime context."""
            return self.close()

    pipeline = Pipeline(BrokenSender(), [SansIOHTTPPolicy()])

    req = HttpRequest("GET", "/")
    with pytest.raises(ValueError):
        pipeline.run(req)

    class SwapExec(SansIOHTTPPolicy):
        def on_exception(self, requests, **kwargs):
            exc_type, exc_value, exc_traceback = sys.exc_info()
            raise NotImplementedError(exc_value)

    pipeline = Pipeline(BrokenSender(), [SwapExec()])
    with pytest.raises(NotImplementedError):
        pipeline.run(req)


class TestRequestsTransport(unittest.TestCase):
    def test_basic_requests(self):

        conf = Configuration()
        request = HttpRequest("GET", "https://bing.com")
        policies = [UserAgentPolicy("myusergant"), RedirectPolicy()]
        with Pipeline(RequestsTransport(conf), policies=policies) as pipeline:
            response = pipeline.run(request)

        assert pipeline._transport.session is None
        assert response.http_response.status_code == 200

    def test_basic_requests_separate_session(self):

        conf = Configuration()
        session = requests.Session()
        request = HttpRequest("GET", "https://bing.com")
        policies = [UserAgentPolicy("myusergant"), RedirectPolicy()]
        transport = RequestsTransport(conf, session=session, session_owner=False)
        with Pipeline(transport, policies=policies) as pipeline:
            response = pipeline.run(request)

        assert transport.session
        assert response.http_response.status_code == 200
        transport.close()
        assert transport.session
        transport.session.close()


class TestClientRequest(unittest.TestCase):
    def test_request_json(self):

        request = HttpRequest("GET", "/")
        data = "Lots of dataaaa"
        request.set_json_body(data)

        self.assertEqual(request.data, json.dumps(data))
        self.assertEqual(request.headers.get("Content-Length"), "17")

    def test_request_data(self):

        request = HttpRequest("GET", "/")
        data = "Lots of dataaaa"
        request.set_bytes_body(data)

        self.assertEqual(request.data, data)
        self.assertEqual(request.headers.get("Content-Length"), "15")

    def test_request_xml(self):
        request = HttpRequest("GET", "/")
        data = ET.Element("root")
        request.set_xml_body(data)

        assert request.data == b"<?xml version='1.0' encoding='utf8'?>\n<root />"

    def test_request_url_with_params(self):

        request = HttpRequest("GET", "/")
        request.url = "a/b/c?t=y"
        request.format_parameters({"g": "h"})

        self.assertIn(request.url, ["a/b/c?g=h&t=y", "a/b/c?t=y&g=h"])


class MockClient:
    def __init__(self, policies=None):
        self.request = HttpRequest("GET", "https://bing.com")
        if policies is None:
            policies = []
        policies.append(mock.Mock(spec=HTTPPolicy, send=self.verify_request))
        self.policies = policies
        self.transport = mock.Mock(spec=HttpTransport)
        self.pipeline = Pipeline(self.transport, policies=policies)

        self.expected_response = mock.Mock(spec=PipelineResponse)

    def verify_request(self, request):
        if len(self.policies) > 1:
            assert request.http_request.headers['span_id'] is not None
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
