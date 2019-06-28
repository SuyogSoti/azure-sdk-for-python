from typing import Any, Callable
import threading
from os import environ
from typing import List
import six

from azure.core.trace.abstract_span import AbstractSpan
from azure.core.trace.ext.opencensus import OpencensusSpan
from azure.core.trace.ext.datadog import DataDogSpan

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
        self.tracing_impl = TracingContext.register_slot("tracing_impl", None)

    def with_current_context(self, func):
        # type: (Callable[Any, Any]) -> Any
        wrapper_class = self.convert_tracing_impl(self.tracing_impl.get())
        if wrapper_class is not None:
            current_impl_span = wrapper_class.get_current_span()
            current_impl_tracer = wrapper_class.get_current_tracer()

        def call_with_current_context(*args, **kwargs):
            if wrapper_class is not None:
                wrapper_class.set_current_span(current_impl_span)
                wrapper_class.set_current_tracer(current_impl_tracer)
                self.current_span.set(wrapper_class(current_impl_span))
            return func(*args, **kwargs)

        return call_with_current_context

    def convert_tracing_impl(self, value):
        # type: (Union[str, AbstractSpan]) -> AbstractSpan
        """Convert a string to a Distributed Tracing Implementation Wrapper

        If a tracing implementation wrapper is passed in, it is returned as-is.
        Otherwise the function understands the following strings, ignoring case:

        * "opencensus"
        * "datadog"

        :param value: the value to convert
        :type value: string
        :returns: AbstractSpan
        :raises ValueError: If conversion to the implementation wrapper fails

        """
        _tracing_implementation = {"opencensus": OpencensusSpan, "datadog": DataDogSpan}
        impl_class = value

        if isinstance(value, six.string_types):
            impl_class = _tracing_implementation.get(value.lower(), None)
            if impl_class is None:
                raise ValueError(
                    "Cannot convert {} to implementation wrapper".format(value)
                )

        return impl_class

    @classmethod
    def register_slot(cls, name, default_val):
        # type: (str, Any) -> ContextProtocol
        return cls._context(name, default_val, cls._lock)


tracing_context = TracingContext()
