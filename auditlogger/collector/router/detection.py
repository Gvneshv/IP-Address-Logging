"""
Router data providers for automatic router detection. Currently a placeholder. Future versions will support vendor-specific integrations.
"""

from .base import RouterProvider


class AutoDetectionProvider(RouterProvider):
    """Automatically detects the router type."""

    def collect(self) -> dict:
        """Collect router information using automatic detection."""

        return {}
