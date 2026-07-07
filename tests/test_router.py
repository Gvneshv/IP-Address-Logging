"""Tests for router provider orchestration."""

from __future__ import annotations
import unittest
from unittest.mock import patch

from auditlogger.collector.router import collect_router_info


class RouterOrchestrationTests(unittest.TestCase):
    """Checks that collect_router_info respects config and delegates to a provider."""

    def test_disabled_router_returns_empty_dict(self) -> None:
        """A disabled router config should never invoke a provider."""
        self.assertEqual(collect_router_info({"enabled": False}), {})

    @patch("auditlogger.collector.router.AutoDetectionProvider.collect", return_value={"wan_ip": "10.0.0.1"})
    def test_enabled_auto_detection_delegates_to_provider(self, _mock_collect) -> None:
        """An enabled auto-detection config should return the provider's collected data."""
        result = collect_router_info({"enabled": True, "detection": {"type": "auto"}})

        self.assertEqual(result, {"wan_ip": "10.0.0.1"})


if __name__ == "__main__":
    unittest.main()