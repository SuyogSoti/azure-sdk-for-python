import threading
from os import environ

from azure.core.trace.abstract_span import AbstractSpan


class TracingContext:
    def __init__(self):
        # type: () -> None
        self.data = threading.local()
        self.lock = threading.Lock()
        with self.lock:
            self.data.current_span = None
        with self.lock:
            self.data.tracer = None

    def set_current_span(self, current_span):
        # type: (AbstractSpan) -> None
        with self.lock:
            self.data.current_span = current_span

    def get_current_span(self):
        # type: () -> AbstractSpan
        return getattr(self.data, "current_span", None)

    def should_only_propagate(self):
        # type: () -> bool
        if "azure_sdk_for_python_only_propagate" in environ:
            return bool(environ["azure_sdk_for_python_only_propagate"])
        return False

    def get_azure_created_tracer(self):
        # type: () -> Any
        return getattr(self.data, "tracer", None)

    def set_tracer(self, tracer):
        # type: (AbstractSpan) -> None
        with self.lock:
            self.data.tracer = tracer


tracing_context = TracingContext()
