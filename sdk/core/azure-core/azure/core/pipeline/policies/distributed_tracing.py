from azure.core.pipeline.policies import SansIOHTTPPolicy
from azure.core.pipeline import PipelineRequest, PipelineResponse
from typing import Any, TypeVar
from abc import abstractmethod

HTTPResponseType = TypeVar("HTTPResponseType")
HTTPRequestType = TypeVar("HTTPRequestType")


class AbstractDistributedTracer(SansIOHTTPPolicy):
    def __init__(
        self,
        name_of_spans="Azure Call",
        header_label="span_id",
        parent_span_param_name="parent_span",
    ):
        # type: (str, str, str) -> None
        self.name_of_child_span = name_of_spans
        self.header_label = header_label
        self.parent_span_param_name = parent_span_param_name
        self.span_dict = {}

    def on_request(self, request, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], Any) -> None
        parent_span = request.context.options.pop(self.parent_span_param_name, None)

        if parent_span is None:
            return

        child = self.create_child_span(parent_span)
        child = self.start_span(child)

        child = self.attach_extra_information(child, request, **kwargs)

        child_span_id = str(self.get_span_id(child))
        self.span_dict[child_span_id] = child
        request.http_request.headers[self.header_label] = child_span_id

    def end_span(self, request):
        # type: (PipelineRequest[HTTPRequestType]) -> Any
        span = None
        span_id = request.http_request.headers.pop(self.header_label, None)
        if span_id is not None:
            span = self.span_dict.pop(span_id, None)
            if span:
                span = self.finish_span(span)

        return span

    def on_response(self, request, response, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], PipelineResponse[HTTPRequestType, HTTPResponseType], Any) -> None
        self.end_span(request)

    def on_exception(self, request, **kwargs):
        # type: (PipelineRequest[HTTPRequestType], Any) -> bool
        self.end_span(request)

    @abstractmethod
    def attach_extra_information(self, child, request, **kwargs):
        # type: (Any, PipelineRequest[HTTPRequestType], Any) -> Any
        raise NotImplementedError

    @abstractmethod
    def create_child_span(self, parent_span):
        # type: (Any) -> Any
        raise NotImplementedError

    @abstractmethod
    def start_span(self, span):
        # type: (Any) -> Any
        raise NotImplementedError

    @abstractmethod
    def get_span_id(self, span):
        # type: (Any) -> str
        raise NotImplementedError

    @abstractmethod
    def finish_span(self, span):
        # type: (Any) -> Any
        raise NotImplementedError


class DistributedTracingOpencensus(AbstractDistributedTracer):
    def __init__(
        self,
        name_of_spans="Azure Call Opencensus",
        header_label="span_id",
        parent_span_param_name="parent_span",
    ):
        # type: (str, str, str) -> None
        AbstractDistributedTracer.__init__(
            self,
            name_of_spans=name_of_spans,
            header_label=header_label,
            parent_span_param_name=parent_span_param_name,
        )

    def attach_extra_information(self, child, request, **kwargs):
        # type: (Any, PipelineRequest[HTTPRequestType], Any) -> Any
        attributes = request.context.options.pop("attributes", None)
        annotations = request.context.options.pop("annotations", None)

        if attributes is not None:
            for key in attributes:
                val = attributes[key]
                child.add_attribute(key, val)

        if annotations is not None:
            for ann in annotations:
                child.add_annotation(ann)

        return child

    def create_child_span(self, parent_span):
        # type: (Any) -> Any
        return parent_span.span(name=self.name_of_child_span)

    def start_span(self, span):
        # type: (Any) -> Any
        span.start()
        return span

    def get_span_id(self, span):
        # type: (Any) -> str
        return span.span_id

    def finish_span(self, span):
        # type: (Any) -> Any
        span.finish()
        return span


class DistributedTracingDataDog(DistributedTracingOpencensus):
    def attach_extra_information(self, child, request, **kwargs):
        # type: (Any, PipelineRequest[HTTPRequestType], Any) -> Any
        tags = request.context.options.pop("tags", None)

        if tags is not None:
            for key in tags:
                val = tags[key]
                child.set_tag(key, val)

        return child

    def start_span(self, span):
        # type: (Any) -> Any
        return span

    def create_child_span(self, parent_span):
        # type: (Any) -> Any
        tracer = parent_span.tracer()
        return tracer.start_span(name=self.name_of_child_span, child_of=parent_span)
