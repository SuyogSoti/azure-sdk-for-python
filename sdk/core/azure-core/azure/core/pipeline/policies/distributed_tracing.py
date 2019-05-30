from azure.core.pipeline import PipelineRequest, PipelineResponse
from azure.core.pipeline.distributed_tracing.context import tracing_context
from azure.core.pipeline.distributed_tracing.span import AbstractSpan, AzureSpan
from azure.core.pipeline.policies import SansIOHTTPPolicy
from typing import Any, TypeVar

HTTPResponseType = TypeVar("HTTPResponseType")
HTTPRequestType = TypeVar("HTTPRequestType")


class DistributedTracer(SansIOHTTPPolicy):
    """The policy to create spans for Azure Calls"""

    def __init__(
        self,
        name_of_spans="Azure Call",
        header_label="distributed_tracing_propagator",
        parent_span_param_name="parent_span",
    ):
        # type: (str, str, str) -> None
        self.name_of_child_span = name_of_spans
        self.header_label = header_label
        self.parent_span_param_name = parent_span_param_name
        self.span_dict = {}

    def on_request(self, request, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], Any) -> None
        parent_span = tracing_context.get_current_span()  # type: AbstractSpan

        if parent_span is None:
            parent_span = AzureSpan(name="parent_of_{}".format(self.name_of_child_span))

        child = parent_span.span(name=self.name_of_child_span)
        child.start()

        # child = self.attach_extra_information(child, request, **kwargs)

        header = child.to_header()
        self.span_dict[header] = child
        request.http_request.headers[self.header_label] = header

    def end_span(self, request):
        # type: (PipelineRequest[HTTPRequestType]) -> Any
        span = None
        header = request.http_request.headers.pop(self.header_label, None)
        if header is not None:
            span = self.span_dict.pop(header, None)  # type: AbstractSpan
            if span:
                span.finish()

        return span

    def on_response(self, request, response, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], PipelineResponse[HTTPRequestType, HTTPResponseType], Any) -> None
        self.end_span(request)

    def on_exception(self, request, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], Any) -> bool
        self.end_span(request)
