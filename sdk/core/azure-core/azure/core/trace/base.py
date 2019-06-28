import functools
from os import environ
import re

from azure.core.trace.context import tracing_context
from azure.core.trace.abstract_span import AbstractSpan
from azure.core.trace.ext.opencensus import OpencensusSpan
from azure.core.settings import settings


def set_span_contexts(span, span_instance=None, wrapper_class=None):
    # type: (AbstractSpan, AbstractSpan) -> None
    tracing_context.current_span.set(span)
    if span is not None or (span_instance is not None and wrapper_class is not None):
        span_instance = span_instance or span.span_instance
        span = wrapper_class or span
        span.set_current_span(span_instance)


def get_parent(kwargs, *args):
    # type: (Any) -> Tuple(Any, Any)
    parent_span = kwargs.pop("parent_span", None)  # type: AbstractSpan
    wrapper_class = tracing_context.convert_tracing_impl(
        settings.tracing_implementation()
    )
    orig_context = tracing_context.current_span.get()

    if parent_span is None:
        parent_span = orig_context
    else:
        wrapper_class = wrapper_class or OpencensusSpan
        parent_span = wrapper_class(parent_span)

    if parent_span is None:
        if wrapper_class is not None:
            current_span = wrapper_class.get_current_span()
            parent_span = (
                wrapper_class(span=current_span)
                if current_span
                else wrapper_class(name="azure-sdk-for-python-first_parent_span")
            )

    original_span_instance = None
    if wrapper_class is not None:
        original_span_instance = wrapper_class.get_current_span()

    return parent_span, orig_context, original_span_instance


def should_use_trace(parent_span, name_of_func):
    # type: (AbstractSpan, List[str], str)
    only_propagate = settings.tracing_should_only_propagate()
    return not (parent_span is None or only_propagate)


def use_distributed_traces(func):
    # type: (Callable[[Any], Any]) -> Callable[[Any], Any]
    @functools.wraps(func)
    def wrapper_use_tracer(self, *args, **kwargs):
        # type: (Any) -> Any
        parent_span, original_span_from_sdk_context, original_span_instance = get_parent(
            kwargs
        )
        ans = None
        if should_use_trace(parent_span, func.__name__):
            set_span_contexts(parent_span)
            name = self.__class__.__name__ + "." + func.__name__
            child = parent_span.span(name=name)
            child.start()
            set_span_contexts(child)
            ans = func(self, *args, **kwargs)
            child.finish()
            set_span_contexts(parent_span)
            if getattr(parent_span, "was_created_by_azure_sdk", False):
                parent_span.finish()
            set_span_contexts(
                original_span_from_sdk_context,
                span_instance=original_span_instance,
                wrapper_class=parent_span,
            )
        else:
            ans = func(self, *args, **kwargs)
        return ans

    return wrapper_use_tracer


def use_distributed_traces_async(func):
    # type: (Callable[[Any], Any]) -> Callable[[Any], Any]
    @functools.wraps(func)
    async def wrapper_use_tracer_async(self, *args, **kwargs):
        # type: (Any) -> Any
        parent_span, original_span_from_sdk_context, original_span_instance = get_parent(
            kwargs
        )
        ans = None
        if should_use_trace(parent_span, func.__name__):
            set_span_contexts(parent_span)
            name = self.__class__.__name__ + "." + func.__name__
            child = parent_span.span(name=name)
            child.start()
            set_span_contexts(child)
            ans = await func(self, *args, **kwargs)
            child.finish()
            set_span_contexts(parent_span)
            if getattr(parent_span, "was_created_by_azure_sdk", False):
                parent_span.finish()
            set_span_contexts(
                original_span_from_sdk_context,
                span_instance=original_span_instance,
                wrapper_class=parent_span,
            )
        else:
            ans = await func(self, *args, **kwargs)
        return ans

    return wrapper_use_tracer_async
