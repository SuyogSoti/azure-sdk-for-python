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

from azure.core.pipeline import Pipeline, use_distributed_traces
from azure.core.pipeline.policies import (
    SansIOHTTPPolicy,
    UserAgentPolicy,
    RedirectPolicy,
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


class MyPipeline:
    def __init__(self, policies=None):
        self.request = HttpRequest("GET", "https://bing.com")
        if policies is None:
            policies = []
        self.transport = RequestsTransport()
        self.pipeline = Pipeline(self.transport, policies=policies)

    @use_distributed_traces
    def run(self, numbTimes, **kwargs):
        if numbTimes < 1:
            return None
        response = self.pipeline.run(self.request, **kwargs)
        self.run(numbTimes - 1, **kwargs)
        return response


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
    def test_with_parent_span_with_opencensus(self):
        pipeline = MyPipeline(policies=[DistributedTracer()])
        parent = ModelOpencensusSpan("Overall")
        attrs = {"firstKey": "firstVal", "secondKey": "secondVal"}
        annotations = ["first Ann", "Second Ann"]
        pipeline.run(
            2, parent_span=parent, tracer="opencensus"
        )
        assert len(parent.children[0].children) == 2
        span = parent.children[0].children[0]
        # TODO(suyogsoti)figure out a way to add annotations
        # assert attrs == span.attrs
        # assert annotations == span.annotations

    def test_with_parent_span_with_datadog(self):
        pipeline = MyPipeline(policies=[DistributedTracer()])
        parent = ModelDataDogSpan("Overall")
        attrs = {"firstKey": "firstVal", "secondKey": "secondVal"}
        pipeline.run(2, parent_span=parent, tracer="datadog")
        print(vars(parent))
        assert len(parent.children[0].children) == 2
        # TODO(suyogsoti)figure out a way to add annotations

    def test_without_parent_span_with_tracing_policies(self):
        pipeline = MyPipeline(policies=[DistributedTracer()])
        pipeline.run(2)
        pipeline = MyPipeline(policies=[DistributedTracer()])
        pipeline.run(2)

    def test_with_parent_span_without_tracing_policies(self):
        pipeline = MyPipeline(policies=[])
        parent = ModelOpencensusSpan("Overall")
        pipeline.run(2, parent_span=parent)
        assert len(parent.children[0].children) == 1

    def test_without_parent_span_without_tracing_policies(self):
        pipeline = MyPipeline(policies=[])
        pipeline.run(2)


if __name__ == "__main__":
    unittest.main()
