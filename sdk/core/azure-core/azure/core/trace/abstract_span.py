from typing import Any, List
from typing_extensions import Protocol


class AbstractSpan(Protocol):
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
        # type: (Dict[str, str]) -> str
        pass

    @staticmethod
    def end_tracer(tracer):
        # type: (Any) -> None
        pass
