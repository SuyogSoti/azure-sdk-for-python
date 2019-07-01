from typing import Any


class AbstractSpan:
    def __init__(self, span=None, name=None):
        # type: (Any, str) -> None
        pass

    def span(self, name="child_span"):
        # type: (str) -> AbstractSpan
        """
        Create a child span for the current span and append it to the child spans list.
         :type name: str
         :param name: (Optional) The name of the child span.
         :rtype: :class: `AbstractSpan`
         :returns: A child Span to be added to the current span.
         """
        pass

    def start(self):
        # type: () -> None
        """Set the start time for a span."""
        pass

    def finish(self):
        # type: () -> None
        """Set the end time for a span."""
        pass

    def to_header(self, headers):
        # type: (Dict[str, str]) -> Dict[str, str]
        pass

    def from_header(self, headers):
        # type: (Dict[str, str]) -> Any
        pass

    @property
    def span_instance(self):
        # type: () -> Any
        pass

    @staticmethod
    def end_tracer(tracer):
        # type: (Any) -> None
        pass

    @staticmethod
    def get_current_span():
        # type: () -> AbstractSpan
        pass

    @staticmethod
    def get_current_tracer():
        # type: () -> Any
        """
        Return if there is no trace in the context currently.
        """
        pass

    @staticmethod
    def set_current_span(span):
        # type: (AbstractSpan) -> None
        pass

    @staticmethod
    def set_current_tracer(tracer):
        # type: (Any) -> None
        pass
