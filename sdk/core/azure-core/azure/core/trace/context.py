from typing_extensions import Protocol
from typing import Any
import threading
from os import environ
from typing import List

from azure.core.trace.abstract_span import AbstractSpan

try:
    import contextvars
except ImportError:
    contextvars = None

__all__ = ["tracing_context"]


class ContextProtocol(Protocol):
    def __init__(self, name, default, lock):
        # type: (string, Any, threading.Lock) -> None
        pass

    def clear(self):
        # type: () -> None
        pass

    def get(self):
        # type: () -> Any
        pass

    def set(self, value):
        # type: (Any) -> None
        pass


class ContextAsyc:
    def __init__(self, name, default, lock):
        self.name = name
        self.contextvar = contextvars.ContextVar(name)
        self.default = default if callable(default) else (lambda: default)
        self.lock = lock

    def clear(self):
        self.contextvar.set(self.default())

    def get(self):
        with self.lock:
            try:
                return self.contextvar.get()
            except LookupError:
                value = self.default()
                self.set(value)
                return value

    def set(self, value):
        self.contextvar.set(value)


class Context:
    _thread_local = threading.local()

    def __init__(self, name, default, lock):
        self.name = name
        self.default = default if callable(default) else (lambda: default)
        self.lock = lock

    def clear(self):
        setattr(self._thread_local, self.name, self.default())

    def get(self):
        with self.lock:
            try:
                return getattr(self._thread_local, self.name)
            except AttributeError:
                value = self.default()
                self.set(value)
                return value

    def set(self, value):
        setattr(self._thread_local, self.name, value)


class TracingContext:
    _lock = threading.Lock()
    _context = ContextAsyc if contextvars else Context

    def __init__(self):
        # type: () -> None
        self.current_span = TracingContext.register_slot("current_span", None)
        self.current_tracer = TracingContext.register_slot("current_tracer", None)

    @classmethod
    def register_slot(cls, name, default_val):
        # type: (str, Any) -> ContextProtocol
        return cls._context(name, default_val, cls._lock)


tracing_context = TracingContext()
