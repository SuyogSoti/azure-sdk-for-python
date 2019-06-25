import functools
from os import environ
import re
import six

from azure.core.trace.context import tracing_context
from azure.core.trace.abstract_span import AbstractSpan
from azure.core.trace.span import OpencensusSpan, DataDogSpan
from azure.core.settings import settings


def convert_tracing_impl(value):
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
        impl_class = _tracing_implementation.get(value, None)
        if impl_class is None:
            raise ValueError(
                "Cannot convert {} to implementation wrapper".format(value)
            )

    return impl_class


def get_parent(kwargs, *args):
    # type: (Any) -> Tuple(Any, Any)
    parent_span = kwargs.pop("parent_span", None)  # type: AbstractSpan
    wrapper_class = convert_tracing_impl(settings.tracing_implementation())
    orig_context = tracing_context.get_current_span()

    if parent_span is None:
        parent_span = orig_context
    else:
        class_to_use = wrapper_class or OpencensusSpan
        parent_span = class_to_use(parent_span)

    if parent_span is None:
        if wrapper_class is not None:
            parent_span = wrapper_class(name="azure-sdk-for-python-first_parent_span")

    tracing_context.set_current_span(parent_span)
    return parent_span, orig_context


def get_blacklist(kwargs, *args):
    # type(Any) -> Tuple(List[str], List[str])
    context_black_list = tracing_context.get_blacklist()
    black_list = kwargs.pop("blacklist", context_black_list)  # type: str
    tracing_context.set_blacklist(black_list)
    return black_list, context_black_list


def reset_context(og_blacklist, original_span_from_context):
    # type: (List[str], Any) -> Any
    tracing_context.set_current_span(original_span_from_context)
    tracing_context.set_blacklist(og_blacklist)


def should_use_trace(parent_span, black_list, name_of_func):
    only_propagate = tracing_context.should_only_propagate()
    is_blacklisted = any([re.match(x, name_of_func) for x in black_list])
    if is_blacklisted:
        tracing_context.set_current_span(None)
    return not (parent_span is None or only_propagate or is_blacklisted)


def use_distributed_traces(func):
    # type: (Callable[[Any], Any]) -> Callable[[Any], Any]
    @functools.wraps(func)
    def wrapper_use_tracer(self, *args, **kwargs):
        # type: (Any) -> Any
        black_list, og_blacklist = get_blacklist(kwargs)
        parent_span, original_span_from_context = get_parent(kwargs)
        ans = None
        if should_use_trace(parent_span, black_list, func.__name__):
            name = self.__class__.__name__ + "." + func.__name__
            child = parent_span.span(name=name)
            child.start()
            tracing_context.set_current_span(child)
            ans = func(self, *args, **kwargs)
            child.finish()
            if getattr(parent_span, "was_created_by_azure_sdk", False):
                parent_span.finish()
        else:
            ans = func(self, *args, **kwargs)
        reset_context(og_blacklist, original_span_from_context)
        return ans

    return wrapper_use_tracer


def use_distributed_traces_async(func):
    # type: (Callable[[Any], Any]) -> Callable[[Any], Any]
    @functools.wraps(func)
    async def wrapper_use_tracer_async(self, *args, **kwargs):
        # type: (Any) -> Any
        black_list, og_blacklist = get_blacklist(kwargs)
        parent_span, original_span_from_context = get_parent(kwargs)
        ans = None
        if should_use_trace(parent_span, black_list, func.__name__):
            name = self.__class__.__name__ + "." + func.__name__
            child = parent_span.span(name=name)
            child.start()
            tracing_context.set_current_span(child)
            ans = await func(self, *args, **kwargs)
            child.finish()
            if getattr(parent_span, "was_created_by_azure_sdk", False):
                parent_span.finish()
        else:
            ans = await func(self, *args, **kwargs)
        reset_context(og_blacklist, original_span_from_context)
        return ans

    return wrapper_use_tracer_async
