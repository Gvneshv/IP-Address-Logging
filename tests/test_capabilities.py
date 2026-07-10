"""Tests for the capability-detection diagnostic summary."""

from __future__ import annotations
import unittest

from auditlogger.main import detect_capabilities


class CapabilityDetectionTests(unittest.TestCase):
    """Checks that detect_capabilities reflects what the network collector returned."""

    def test_all_capabilities_true_when_everything_present(self) -> None:
        """A fully-populated network_info with router.enabled should report all True."""
        config = {"router": {"enabled": True, "detection": {"type": "tplink"}}}
        network_info = {
            "external_ip": "203.0.113.10",
            "router": {"wan_ip": "198.51.100.1"},
        }

        capabilities = detect_capabilities(config, network_info)

        self.assertEqual(
            capabilities,
            {
                "public_ip_lookup": True,
                "router_enabled": True,
                "router_detected": True,
                "router_vendor": "tplink",
                "wan_ip_supported": True,
            },
        )

    def test_disabled_router_reports_no_vendor(self) -> None:
        """A disabled router should report router_vendor as None even if configured."""
        config = {"router": {"enabled": False, "detection": {"type": "tplink"}}}
        network_info = {"external_ip": "203.0.113.10"}

        capabilities = detect_capabilities(config, network_info)

        self.assertFalse(capabilities["router_enabled"])
        self.assertIsNone(capabilities["router_vendor"])
        self.assertFalse(capabilities["router_detected"])
        self.assertFalse(capabilities["wan_ip_supported"])

    def test_missing_external_ip_reports_lookup_unavailable(self) -> None:
        """A null external_ip (all endpoints failed) should report public_ip_lookup as False."""
        capabilities = detect_capabilities({"router": {}}, {"external_ip": None})

        self.assertFalse(capabilities["public_ip_lookup"])


if __name__ == "__main__":
    unittest.main()