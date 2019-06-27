import copy
from typing import Any
from azure.core.trace.context import tracing_context
from azure.core.settings import settings


class OpencensusSpan:
    def __init__(self, span=None, name="parent_span"):
        # type: (Any) -> None
        from opencensus.trace import tracer as tracer_module, Span
        from opencensus.trace.samplers import ProbabilitySampler

        tracer = OpencensusSpan.get_current_tracer()
        self.was_created_by_azure_sdk = False
        if span is None:
            instrumentation_key = settings.tracing_istrumentation_key()
            prob = settings.tracing_sampler()
            if tracer is None:
                if instrumentation_key is not None:
                    from opencensus.ext.azure.trace_exporter import AzureExporter

                    tracer = tracer_module.Tracer(
                        exporter=AzureExporter(instrumentation_key=instrumentation_key),
                        sampler=ProbabilitySampler(prob),
                    )
                else:
                    tracer = tracer_module.Tracer(sampler=ProbabilitySampler(prob))
                self.was_created_by_azure_sdk = True
            span = tracer.span(name=name)

        self.tracer = tracer
        self.trace_id = None
        if span.context_tracer:
            self.trace_id = span.context_tracer.span_context.trace_id
        self.span_instance = span
        self.span_id = str(span.span_id)
        self.children = []
        self.impl_library = "opencensus"

    def span(self, name="child_span"):
        # type: (str) -> OpencensusSpan
        child = self.span_instance.span(name=name)
        wrapped_child = OpencensusSpan(child)
        wrapped_child.trace_id = self.trace_id
        self.children.append(wrapped_child)
        return wrapped_child

    def start(self):
        # type: () -> None
        self.span_instance.start()

    def finish(self):
        # type: () -> None
        self.span_instance.finish()
        if self.was_created_by_azure_sdk:
            self.end_tracer(self.tracer)

    def to_header(self, headers):
        # type: (Dict[str, str]) -> str
        tracer_from_context = OpencensusSpan.get_current_tracer()
        header = ""
        if tracer_from_context is not None:
            ctx = copy.deepcopy(tracer_from_context.span_context)
            ctx.span_id = self.span_id
            header = "{}-{}".format(ctx.span_id, ctx.trace_id)
            tempDict = tracer_from_context.propagator.to_headers(ctx)
            headers.update(tempDict)
        return header

    @staticmethod
    def end_tracer(tracer):
        # type: (Tracer) -> None
        if tracer is not None:
            tracer.end_span()

    @staticmethod
    def get_current_span():
        # type: () -> AbstractSpan
        from opencensus.trace import execution_context

        return execution_context.get_current_span()

    @staticmethod
    def get_current_tracer():
        # type: () -> Any
        from opencensus.trace import execution_context

        return execution_context.get_opencensus_tracer()

    @staticmethod
    def set_current_span(span):
        # type: (Span) -> None
        from opencensus.trace import execution_context

        return execution_context.set_current_span(span)

    @staticmethod
    def set_current_tracer(tracer):
        # type: (Any) -> None
        from opencensus.trace import execution_context

        return execution_context.set_opencensus_tracer(span)


class DataDogSpan:
    def __init__(self, span=None, name=None):
        # type: (Any) -> None
        from ddtrace import tracer

        self.was_created_by_azure_sdk = False

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

    @staticmethod
    def get_current_span():
        # type: () -> AbstractSpan
        from ddtrace import tracer

        return tracer.current_span()

    @staticmethod
    def get_current_tracer():
        # type: () -> tracer.Tracer
        return DataDogSpan.get_current_span.tracer()

    @staticmethod
    def set_current_span(span):
        # type: (Span) -> None
        pass

    @staticmethod
    def set_current_tracer(tracer):
        # type: (Any) -> None
        pass
