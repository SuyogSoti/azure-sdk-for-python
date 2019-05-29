import threading

from azure.core.pipeline.distributed_tracing.span import AbstractSpan


class TracingContext:
    def __init__(self):
        # type: () -> None
        self.data = {}
        self._lock = threading.Lock()

    def set_current_span(self, current_span):
        # type: (AbstractSpan) -> None
        self._lock.acquire()
        self.data['current_span'] = current_span
        self._lock.release()

    def get_current_span(self):
        # type: () -> AbstractSpan
        if "current_span" not in self.data:
            return None
        return self.data['current_span']


tracing_context = TracingContext()
