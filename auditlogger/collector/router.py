from __future__ import annotations

from typing import Any
from providers.detection import AutoDetectionProvider


def _detect_router_type():
    """Detect the router implementation."""
    return None


def _collect_router_data():
    """Collect data from the configured router."""
    return {}


def collect_router_info(router_config: dict[str, Any]) -> dict[str, Any]:
    """
    Collect information from the configured router.

    Currently this collector is a placeholder and always returns an empty dictionary.

    Future versions will support automatic router detection and vendor-specific integrations.
    """
    if not router_config.get("enabled", False):
        return {}
    
    match router_config.get("type", "auto"):
        case "auto":
            provider = AutoDetectionProvider(...)
        case _:
            return {}

    return {}