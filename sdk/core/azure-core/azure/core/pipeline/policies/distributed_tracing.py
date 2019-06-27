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

    def __init__(
        self,
        name_of_spans="Azure Call",
        header_label="distributed_tracing_propagator",
    ):
        # type: (str, str, str) -> None
        self.name_of_child_span = name_of_spans
        self.header_label = header_label
        self.parent_span = None
        self.span_dict = {}

    def set_header(self, request, span):
        # type: (PipelineRequest[HTTPRequestType], Any) -> None
        """
        Sets the header information on the span.
        """
        header = span.to_header(request.http_request.headers)
        self.span_dict[header] = span
        request.http_request.headers[self.header_label] = header

    def on_request(self, request, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], Any) -> None
        parent_span = tracing_context.current_span.get()  # type: AbstractSpan

        self.parent_span = parent_span
        if parent_span is None:
            return

        only_propagate = settings.tracing_should_only_propagate()
        if only_propagate:
            self.set_header(request, parent_span)
            return


        child = parent_span.span(name=self.name_of_child_span)
        child.start()
        
        set_span_contexts(child)
        # child = self.attach_extra_information(child, request, **kwargs)
        self.set_header(request, child)

    def end_span(self, request):
        # type: (PipelineRequest[HTTPRequestType]) -> Any
        span = None
        header = request.http_request.headers.pop(self.header_label, None)
        if header is not None:
            span = self.span_dict.pop(header, None)  # type: AbstractSpan
            only_propagate = settings.tracing_should_only_propagate()
            if span and not only_propagate:
                span.finish()
        set_span_contexts(self.parent_span)
        return span

    def on_response(self, request, response, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], PipelineResponse[HTTPRequestType, HTTPResponseType], Any) -> None
        self.end_span(request)

    def on_exception(self, request, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], Any) -> bool
        self.end_span(request)
