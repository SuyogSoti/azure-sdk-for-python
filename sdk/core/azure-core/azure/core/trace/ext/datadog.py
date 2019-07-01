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
        return headers
    
    def from_header(self, headers):
        # type: (Dict[str, str]) -> Any
        from ddtrace.propagation.http import HTTPPropagator
        from ddtrace import tracer

        propogator = HTTPPropagator()
        ctx = propogator.extract(headers)
        tracer.context_provider.activate(ctx)
        return tracer

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
