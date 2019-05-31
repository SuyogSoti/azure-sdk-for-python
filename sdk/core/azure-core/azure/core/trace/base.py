import functools

from azure.core.trace.context import tracing_context
from azure.core.trace.span import OpenCensusSpan, DataDogSpan


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

        if parent_span is None:
            parent_span = tracing_context.get_current_span()
        else:
            tracer_dict = {
                "opencensus": OpenCensusSpan,
                'datadog': DataDogSpan
            }
            abs_class = tracer_dict.get(tracer_impl, OpenCensusSpan)
            parent_span = abs_class(parent_span)

        ans = None
        if parent_span is None:
            ans = func(self, *args, **kwargs)
        else:
            child = parent_span.span(name=name)
            child.start()
            tracing_context.set_current_span(child)
            ans = func(self, *args, **kwargs)
            child.finish()
        return ans

    return wrapper_use_tracer