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


class AzureSpan():
    def __init__(self, name="span"):
        # type: (str) -> None
        self.span_id = str(randint(1000000, 10000000)) + "-" + str(time.time())
        self.name = name
        self.start_time = time.time()
        self.attrs = {}
        self.annotations = {}
        self.children = []
        self.end_time = None
        self.parent_span = None

    def span(self, name="child_span"):
        # type: (str) -> AzureSpan
        child = AzureSpan(name=name)
        child.parent_span = self
        self.children.append(child)
        return child

    def start(self, start_time=None):
        # type: () -> None
        if start_time is None:
            self.start_time = time.time()
        else:
            self.start_time = start_time

    def add_attribute(self, key, val):
        # type: (str, str) -> None
        self.attrs[key] = val

    def add_annotation(self, descp, **attrs):
        # type: (str, Any) -> None
        self.annotations[time.time()] = descp

    def finish(self, end_time=None):
        # type: () -> None
        if end_time is None:
            self.end_time = time.time()
        else:
            self.end_time = end_time

    def to_header(self):
        # type: () -> bytes
        return str(vars(self))


class OpenCensusSpan:
    def __init__(self, span):
        # type: (Any) -> None
        self.span_instance = span
        self.span_id = str(span.span_id)

    def span(self, name="child_span"):
        # type: (str) -> OpenCensusSpan
        child = self.span_instance.span(name=name)
        return OpenCensusSpan(child)

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
        # type: () -> bytes
        return str(vars(self.span_instance))


class DataDogSpan:

    def __init__(self, span):
        # type: (Any) -> None
        self.span_instance = span
        self.span_id = str(span.span_id)

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
        # type: () -> bytes
        props = dir(self.span_instance)
        string = str([getattr(self.span_instance, prop, None) for prop in props])
        return string
