"""Base interface for router data providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RouterProvider(ABC):
    """Common interface every router provider (auto-detected or vendor-specific) must implement."""

    @abstractmethod
    def collect(self) -> dict[str, Any]:
        """Return the router fields this provider can collect (e.g. WAN IP, DNS, gateway)."""
