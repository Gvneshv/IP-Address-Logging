"""Base interface for router data providers."""


from abc import ABC, abstractmethod
from typing import Any


class RouterProvider(ABC):
    """Base interface for router data providers.
    Collects router information."""

    @abstractmethod
    def collect(self) -> dict[str, Any]:
        """Collect router information."""