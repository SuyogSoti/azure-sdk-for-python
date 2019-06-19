import copy
import os
from typing import Any
from azure.core.trace.context import tracing_context


class OpenCensusSpan:
    def __init__(self, span=None, name=None):
        # type: (Any) -> None
        from opencensus.trace import tracer as tracer_module, execution_context, Span

        self.execution_context = execution_context

        if span is None:
            span = self.execution_context.get_current_span()

        tracer = tracing_context.get_azure_created_tracer()
        self.was_created_by_azure_sdk = False
        # Attact an exporter here from environmental variable
        if span is None:
            if name is None:
                name = "parent_span"
            if "APPINSIGHTS_INSTRUMENTATIONKEY" in os.environ:
                if tracer is None:
                    from opencensus.ext.azure.trace_exporter import AzureExporter
                    from opencensus.trace.samplers import ProbabilitySampler

                    prob = 0.001
                    if "azure_sdk_for_python_sampler" in os.environ:
                        prob = os.environ["azure_sdk_for_python_sampler"]
                    tracer = tracer_module.Tracer(
                        exporter=AzureExporter(
                            instrumentation_key=os.environ[
                                "APPINSIGHTS_INSTRUMENTATIONKEY"
                            ]
                        ),
                        sampler=ProbabilitySampler(float(prob)),
                    )
                    tracing_context.set_tracer(tracer)
                    self.was_created_by_azure_sdk = True
                span = tracer.span(name=name)
            else:
                span = Span(name=name)

        self.span_instance = span
        self.trace_id = None
        if span.context_tracer:
            self.trace_id = span.context_tracer.trace_id
        self.span_id = str(span.span_id)
        self.children = []
        self.impl_library = "opencensus"

    def span(self, name="child_span"):
        # type: (str) -> OpenCensusSpan
        child = self.span_instance.span(name=name)
        wrapped_child = OpenCensusSpan(child)
        wrapped_child.trace_id = self.trace_id
        self.children.append(wrapped_child)
        return wrapped_child

    def start(self):
        # type: () -> None
        self.span_instance.start()

    def finish(self):
        # type: () -> None
        self.span_instance.finish()

    def add_attribute(self, key, val):
        # type: (str, str) -> None
        self.span_instance.add_attribute(key, val)

    def add_annotation(self, ann, **attrs):
        # type: (str, Any) -> None
        self.span_instance.add_annotation(ann, **attrs)

    def to_header(self, headers):
        # type: (Dict[str, str]) -> str
        tracer_from_context = self.get_current_trace_from_context()
        header = ""
        if tracer_from_context is not None:
            ctx = copy.deepcopy(tracer_from_context.span_context)
            ctx.span_id = self.span_id
            header = "{}-{}".format(ctx.span_id, ctx.trace_id)
            tempDict = tracer_from_context.propagator.to_headers(ctx)
            headers.update(tempDict)
        return header

    def get_current_span_from_context(self):
        # type: () -> Span
        return self.execution_context.get_current_span()

    def get_current_trace_from_context(self):
        # type: () -> Tracer
        return self.execution_context.get_opencensus_tracer()

    @staticmethod
    def end_tracer(tracer):
        # type: (Tracer) -> None
        if tracer is not None:
            tracer.end_span()


class DataDogSpan:
    def __init__(self, span=None, name=None):
        # type: (Any) -> None
        from ddtrace import tracer

        self.was_created_by_azure_sdk = False
        if span is None:
            span = tracer.current_span()

        if span is None:
            if name is None:
                name = "parent_span"
            span = tracer.trace(name=name, service="Azure Python SDK Default")
            self.was_created_by_azure_sdk = True

        self.span_instance = span
        self.span_id = str(span.span_id)
        self.trace_id = span.trace_id
        self.children = []
        self.impl_library = "datadog"

    def span(self, name="child_span"):
        # type: (str) -> DataDogSpan
        tracer = self.span_instance.tracer()
        wrapper_span = DataDogSpan(
            tracer.start_span(name=name, child_of=self.span_instance)
        )
        self.children.append(wrapper_span)
        return wrapper_span

    def start(self):
        # type: () -> None
        pass

    def finish(self):
        # type: () -> None
        self.span_instance.finish()

    def add_attribute(self, key, val):
        # type: (str, str) -> None
        self.span_instance.set_tag(key, val)

    def add_annotation(self, ann, **attrs):
        # type: (str, Any) -> None
        pass

    def to_header(self, headers):
        # type: (Dict[str, str]) -> str
        from ddtrace.propagation.http import HTTPPropagator

        propogator = HTTPPropagator()
        propogator.inject(self.span_instance.context, headers)
        return "{}-{}".format(self.span_id, self.trace_id)

    @staticmethod
    def end_tracer(tracer):
        # type: (Tracer) -> None
        pass


SUPPORTED_TRACE_IMPLEMENTATIONS = {"opencensus": OpenCensusSpan, "datadog": DataDogSpan}
