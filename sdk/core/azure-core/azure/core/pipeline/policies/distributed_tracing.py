from azure.core.pipeline import PipelineRequest, PipelineResponse
from azure.core.trace.context import tracing_context
from azure.core.trace.abstract_span import AbstractSpan
from azure.core.trace.base import set_span_contexts
from azure.core.pipeline.policies import SansIOHTTPPolicy
from azure.core.settings import settings
from typing import Any, TypeVar

HTTPResponseType = TypeVar("HTTPResponseType")
HTTPRequestType = TypeVar("HTTPRequestType")


class DistributedTracer(SansIOHTTPPolicy):
    """The policy to create spans for Azure Calls"""

    def __init__(self, name_of_spans="Azure Call"):
        # type: (str, str, str) -> None
        self.name_of_child_span = name_of_spans
        self.parent_span_dict = {}

    def set_header(self, request, span):
        # type: (PipelineRequest[HTTPRequestType], Any) -> None
        """
        Sets the header information on the span.
        """
        headers = span.to_header(request.http_request.headers)
        request.http_request.headers.update(headers)

    def on_request(self, request, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], Any) -> None
        parent_span = tracing_context.current_span.get()  # type: AbstractSpan

        if parent_span is None:
            return

        only_propagate = settings.tracing_should_only_propagate()
        if only_propagate:
            self.set_header(request, parent_span)
            return

        child = parent_span.span(name=self.name_of_child_span)
        child.start()

        set_span_contexts(child)
        self.parent_span_dict[child] = parent_span
        self.set_header(request, child)

    def end_span(self):
        # type: (PipelineRequest[HTTPRequestType]) -> None
        span = tracing_context.current_span.get()
        only_propagate = settings.tracing_should_only_propagate()
        if span and not only_propagate:
            span.finish()
            set_span_contexts(self.parent_span_dict[span])

    def on_response(self, request, response, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], PipelineResponse[HTTPRequestType, HTTPResponseType], Any) -> None
        self.end_span()

    def on_exception(self, request, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], Any) -> bool
        self.end_span()
