from typing import Any, Callable
import threading
from os import environ
from typing import List

from azure.core.trace.abstract_span import AbstractSpan

try:
    import contextvars
except ImportError:
    contextvars = None

__all__ = ["tracing_context"]


class ContextProtocol:
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
        try:
            return self.contextvar.get()
        except LookupError:
            value = self.default()
            self.set(value)
            return value

    def set(self, value):
        with self.lock:
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
        try:
            return getattr(self._thread_local, self.name)
        except AttributeError:
            value = self.default()
            self.set(value)
            return value

    def set(self, value):
        with self.lock:
            setattr(self._thread_local, self.name, value)


class TracingContext:
    _lock = threading.Lock()
    _context = ContextAsyc if contextvars else Context

    def __init__(self):
        # type: () -> None
        self.current_span = TracingContext.register_slot("current_span", None)

    def with_current_context(self, func):
        # type: (Callable[Any, Any]) -> Any
        caller_context = self.get_snapshot()

        def call_with_current_context(*args, **kwargs):
            try:
                backup_context = self.get_snapshot()
                self.apply(caller_context)
                return func(*args, **kwargs)
            finally:
                self.apply(backup_context)

        return call_with_current_context

    def apply(self, contexts):
        for key in contexts:
            val = contexts[key]
            attr = getattr(self, key)
            attr.set(val)

    def get_snapshot(self):
        # type: () -> Dict[str, Any]
        attrs = vars(self)
        new_dict = {}
        for key in attrs:
            if isinstance(attrs[key], TracingContext._context):
                new_dict[key] = attrs[key].get()
        return new_dict

    @classmethod
    def register_slot(cls, name, default_val):
        # type: (str, Any) -> ContextProtocol
        return cls._context(name, default_val, cls._lock)


tracing_context = TracingContext()
