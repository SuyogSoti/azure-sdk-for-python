from typing import Any
import os


class OpencensusSpan:
    def __init__(self, span=None, name="parent_span"):
        # type: (Any) -> None
        from opencensus.trace import tracer as tracer_module, Span
        from opencensus.trace.tracers.noop_tracer import NoopTracer
        from opencensus.trace.samplers import ProbabilitySampler

        tracer = OpencensusSpan.get_current_tracer()
        self.was_created_by_azure_sdk = False
        if span is None:
            instrumentation_key = self._get_environ("APPINSIGHTS_INSTRUMENTATIONKEY")
            prob = self._get_environ("AZURE_TRACING_SAMPLER") or 0.001
            if tracer is None or isinstance(tracer, NoopTracer):
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

    def _get_environ(self, key):
        # type: (str) -> str
        if key in os.environ:
            return os.environ[key]
        return None

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
        temp_headers = {}
        if tracer_from_context is not None:
            ctx = tracer_from_context.span_context
            temp_headers = tracer_from_context.propagator.to_headers(ctx)
        return temp_headers
    
    def from_header(self, headers):
        # type: (Dict[str, str]) -> Any
        from opencensus.trace import tracer as tracer_module
        from opencensus.trace.propagation import trace_context_http_header_format
        ctx = trace_context_http_header_format.TraceContextPropagator().from_headers(headers)
        return tracer_module.Tracer(span_context=ctx)

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

        return execution_context.set_opencensus_tracer(tracer)
