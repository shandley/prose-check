from abc import ABC, abstractmethod

from .._models import DocumentContext, Finding


class Checker(ABC):
    """Base class for all prose quality checkers."""

    name: str  # subclasses must set this as a class attribute

    @abstractmethod
    def check(self, text: str, context: DocumentContext) -> list[Finding]:
        """Check text and return a list of findings."""
        ...
