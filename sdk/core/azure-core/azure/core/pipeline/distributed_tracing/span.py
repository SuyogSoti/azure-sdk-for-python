import time
from random import randint

from typing import Any
from typing_extensions import Protocol


class AbstractSpan(Protocol):
    @property
    def span_id(self):
        # type: () -> str
        pass

    def span(self, name="child_span"):
        # type: (str) -> AbstractSpan
        """Create a child span for the current span and append it to the child
        spans list.

        :type name: str

        :param name: (Optional) The name of the child span.

        :rtype: :class: `AbstractSpan`

        :returns: A child Span to be added to the current span.

        """
        pass

    def add_attribute(self, attribute_key, attribute_value):
        # type: (str, str) -> None
        """Add attribute to span.

        :type attribute_key: str

        :param attribute_key: Attribute key.



        :type attribute_value:str

        :param attribute_value: Attribute value.

        """
        pass

    def add_annotation(self, description, **attrs):
        # type: (str, Any) -> None
        """Add an annotation to span.

        :type description: str

        :param description: A user-supplied message describing the event.

                        The maximum length for the description is 256 bytes.


        :type attrs: kwargs

        :param attrs: keyworded arguments e.g. failed=True, name='Caching'

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

    def to_header(self):
        # type: () -> str
        pass


class OpenCensusSpan:
    def __init__(self, span):
        # type: (Any) -> None
        self.span_instance = span
        self.trace_id = None
        if span.context_tracer:
            self.trace_id = span.context_tracer.trace_id
        self.span_id = str(span.span_id)

    def span(self, name="child_span"):
        # type: (str) -> OpenCensusSpan
        child = self.span_instance.span(name=name)
        wrapped_child = OpenCensusSpan(child)
        wrapped_child.trace_id = self.trace_id
        return wrapped_child

    def start(self):
        # type: () -> None
        self.span_instance.start()

    def finish(self):
        # type: () -> None
        self.span_instance.finish()

    def add_attribute(self, key, val):
        # type: (str, str) -> None
        self.span_instance.add_attribute(key, val)

    def add_annotation(self, ann, **attrs):
        # type: (str, Any) -> None
        self.span_instance.add_annotation(ann, **attrs)

    def to_header(self):
        # type: () -> str
        return "{},{}".format(self.span_id, self.trace_id)


class DataDogSpan:
    def __init__(self, span):
        # type: (Any) -> None
        self.span_instance = span
        self.span_id = str(span.span_id)
        self.trace_id = span.trace_id

    def span(self, name="child_span"):
        # type: (str) -> DataDogSpan
        tracer = self.span_instance.tracer()
        return DataDogSpan(tracer.start_span(name=name, child_of=self.span_instance))

    def start(self):
        # type: () -> None
        pass

    def finish(self):
        # type: () -> None
        self.span_instance.finish()

    def add_attribute(self, key, val):
        # type: (str, str) -> None
        self.span_instance.set_tag(key, val)

    def add_annotation(self, ann, **attrs):
        # type: (str, Any) -> None
        pass

    def to_header(self):
        # type: () -> str
        return "{},{}".format(self.span_id, self.trace_id)
