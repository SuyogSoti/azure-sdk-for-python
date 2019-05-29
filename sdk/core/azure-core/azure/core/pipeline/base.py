# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# --------------------------------------------------------------------------

import functools
import logging

from azure.core.pipeline import (
    AbstractContextManager,
    PipelineRequest,
    PipelineResponse,
    PipelineContext,
)
from azure.core.pipeline.distributed_tracing.context import tracing_context
from azure.core.pipeline.distributed_tracing.span import AbstractSpan, AzureSpan, OpenCensusSpan, DataDogSpan
from azure.core.pipeline.policies import HTTPPolicy, SansIOHTTPPolicy
from typing import (
    Generic,
    TypeVar,
    List,
    Union,
    Any,
    # pylint: disable=unused-import
    Callable,
)

HTTPResponseType = TypeVar("HTTPResponseType")
HTTPRequestType = TypeVar("HTTPRequestType")
HttpTransportType = TypeVar("HttpTransportType")

_LOGGER = logging.getLogger(__name__)
PoliciesType = List[Union[HTTPPolicy, SansIOHTTPPolicy]]


def use_distributed_traces(func):
    # type: (Callable[[Any], Any]) -> Callable[[Any], Any]
    @functools.wraps(func)
    def wrapper_use_tracer(self, *args, **kwargs):
        # type: (Any) -> Any

        name = (
                self.__class__.__name__
                + "."
                + func.__name__
                + "("
                + ", ".join([str(i) for i in args])
                + ")"
        )

        parent_span = kwargs.pop("parent_span", None)  # type: AbstractSpan
        tracer_impl = kwargs.pop("tracer", None)  # type: str

        if parent_span is None:
            parent_span = tracing_context.get_current_span()
        else:
            tracer_dict = {
                "opencensus": OpenCensusSpan,
                'datadog': DataDogSpan
            }
            abs_class = tracer_dict.get(tracer_impl, OpenCensusSpan)
            parent_span = abs_class(parent_span)

        if parent_span is None:
            parent_span = AzureSpan(name="use_distributed_traces_decorator")

        # not all functions will take in parent_span
        child = parent_span.span(name=name)
        child.start()
        tracing_context.set_current_span(child)
        ans = func(self, *args, **kwargs)
        child.finish()

        return ans

    return wrapper_use_tracer


class _SansIOHTTPPolicyRunner(HTTPPolicy, Generic[HTTPRequestType, HTTPResponseType]):
    """Sync implementation of the SansIO policy.
    """

    def __init__(self, policy):
        # type: (SansIOHTTPPolicy) -> None
        super(_SansIOHTTPPolicyRunner, self).__init__()
        self._policy = policy

    def send(self, request):
        # type: (PipelineRequest) -> PipelineResponse
        self._policy.on_request(request)
        try:
            response = self.next.send(request)
        except Exception:  # pylint: disable=broad-except
            if not self._policy.on_exception(request):
                raise
        else:
            self._policy.on_response(request, response)
        return response


class _TransportRunner(HTTPPolicy):
    def __init__(self, sender):
        # type: (HttpTransportType) -> None
        super(_TransportRunner, self).__init__()
        self._sender = sender

    def send(self, request):
        return PipelineResponse(
            request.http_request,
            self._sender.send(request.http_request, **request.context.options),
            context=request.context,
        )


class Pipeline(AbstractContextManager, Generic[HTTPRequestType, HTTPResponseType]):
    """A pipeline implementation.

    This is implemented as a context manager, that will activate the context
    of the HTTP sender.
    """

    def __init__(self, transport, policies=None):
        # type: (HttpTransportType, PoliciesType) -> None
        self._impl_policies = []  # type: List[HTTPPolicy]
        self._transport = transport  # type: ignore

        for policy in policies or []:
            if isinstance(policy, SansIOHTTPPolicy):
                self._impl_policies.append(_SansIOHTTPPolicyRunner(policy))
            elif policy:
                self._impl_policies.append(policy)
        for index in range(len(self._impl_policies) - 1):
            self._impl_policies[index].next = self._impl_policies[index + 1]
        if self._impl_policies:
            self._impl_policies[-1].next = _TransportRunner(self._transport)

    def __enter__(self):
        # type: () -> Pipeline
        self._transport.__enter__()  # type: ignore
        return self

    def __exit__(self, *exc_details):  # pylint: disable=arguments-differ
        self._transport.__exit__(*exc_details)

    def run(self, request, **kwargs):
        # type: (HTTPRequestType, Any) -> PipelineResponse
        context = PipelineContext(self._transport, **kwargs)
        pipeline_request = PipelineRequest(
            request, context
        )  # type: PipelineRequest[HTTPRequestType]
        first_node = (
            self._impl_policies[0]
            if self._impl_policies
            else _TransportRunner(self._transport)
        )
        return first_node.send(pipeline_request)  # type: ignore
