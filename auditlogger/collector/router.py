from __future__ import annotations

from typing import Any


def collect_router_info(config: dict[str, Any]) -> dict[str, Any]:
    """
    Collect information from the configured router.

    Currently this collector is a placeholder and always returns an empty dictionary.

    Future versions will support automatic router detection and vendor-specific integrations.
    """
    return {}