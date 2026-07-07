"""Router provider orchestration: select a provider and collect router data.

This is the single entry point the rest of the application should use for router information.
Callers (e.g. the network collector) should never import a specific provider such as AutoDetectionProvider directly - collect_router_info() owns the decision of which provider to use, so that decision only has to change in one place as vendor providers are added.
"""

from __future__ import annotations

from typing import Any

from .detection import AutoDetectionProvider


def _select_provider(router_config: dict[str, Any]):
    """Return the RouterProvider instance for the configured detection type."""
    detection_type = router_config.get("detection", {}).get("type", "auto")

    match detection_type:
        case "auto":
            return AutoDetectionProvider()
        case _:
            # Vendor-specific providers (tplink, mikrotik, asus, keenetic) will
            # be added as new cases here once implemented. Unknown/unsupported
            # types fall back to auto-detection rather than failing outright.
            return AutoDetectionProvider()


def collect_router_info(router_config: dict[str, Any]) -> dict[str, Any]:
    """Collect router information using the configured provider.

    Returns an empty dict when the router feature is disabled, matching the"collectors fail/opt-out independently without breaking the snapshot"
    principle described in docs/architecture.md.
    """
    if not router_config.get("enabled", False):
        return {}

    provider = _select_provider(router_config)
    return provider.collect()
