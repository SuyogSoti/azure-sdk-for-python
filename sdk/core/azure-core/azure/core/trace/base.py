import functools
from os import environ
import re

from azure.core.trace.context import tracing_context
from azure.core.trace.abstract_span import AbstractSpan
from azure.core.trace.span import SUPPORTED_TRACE_IMPLEMENTATIONS, OpenCensusSpan


def use_distributed_traces(func):
    # type: (Callable[[Any], Any]) -> Callable[[Any], Any]
    @functools.wraps(func)
    def wrapper_use_tracer(self, *args, **kwargs):
        # type: (Any) -> Any

        name = (
            self.__class__.__name__
            + "."
            + func.__name__
            + "("
            + ", ".join([str(i) for i in args])
            + ")"
        )

        parent_span = kwargs.pop("parent_span", None)  # type: AbstractSpan
        tracer_impl = kwargs.pop("tracer", None)  # type: str
        black_list = kwargs.pop("blacklist", None)  # type: str

        if "azure_sdk_for_python_tracer" in environ:
            tracer_impl = environ["azure_sdk_for_python_tracer"]

        tracer_dict = SUPPORTED_TRACE_IMPLEMENTATIONS
        orig_context = tracing_context.get_current_span()

        if parent_span is None:
            parent_span = orig_context
        else:
            abs_class = tracer_dict.get(tracer_impl, OpenCensusSpan)
            parent_span = abs_class(parent_span)

        if parent_span is None:
            abs_class = tracer_dict.get(tracer_impl, None)
            if abs_class is not None:
                parent_span = abs_class(name="azure-sdk-for-python-first_parent_span")

        ans = None
        tracing_context.set_current_span(parent_span)
        only_propagate = tracing_context.should_only_propagate()
        if (
            parent_span is None
            or only_propagate
            or any([re.match(x, func.__name__) for x in black_list])
        ):
            ans = func(self, *args, **kwargs)
        else:
            child = parent_span.span(name=name)
            child.start()
            tracing_context.set_current_span(child)
            ans = func(self, *args, **kwargs)
            child.finish()
            # FIXME: This monkey patch is meh
            if parent_span.was_created_by_azure_sdk:
                old_del = getattr(self, "__del__", None)
                old_type = type(self)
                self.__class__ = type(
                    old_type.__name__ + "_Override",
                    (old_type,),
                    delete_monkey_patcher(func=old_del, current_span=parent_span),
                )
        tracing_context.set_current_span(orig_context)
        return ans

    return wrapper_use_tracer


def delete_monkey_patcher(func, current_span):
    # type: (Callable[[Any], Any]) -> Callable[[Any], Any]
    @functools.wraps(func)
    def wrapper_end_tracer(self, *args, **kwargs):
        ans = None
        if func is not None:
            ans = func(self, *args, **kwargs)
        tracer = tracing_context.get_azure_created_tracer()
        current_span.end_tracer(tracer)
        return ans

    return {"__del__": wrapper_end_tracer}
