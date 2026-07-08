"""Tests for the notification-trigger decision logic in main.py."""

from __future__ import annotations
import unittest

from auditlogger.main import _detect_notifiable_changes


class NotificationTriggerTests(unittest.TestCase):
    """Checks that _detect_notifiable_changes respects per-trigger config."""

    def test_defaults_detect_both_external_ip_and_wan_changes(self) -> None:
        """With no notify_on config, both known triggers should be enabled by default."""
        previous_network = {"external_ip": "203.0.113.10", "router": {"wan_ip": "198.51.100.1"}}
        current_network = {"external_ip": "203.0.113.11", "router": {"wan_ip": "198.51.100.2"}}

        changes = _detect_notifiable_changes({}, previous_network, current_network)

        self.assertIn(("external_ip", "203.0.113.10", "203.0.113.11"), changes)
        self.assertIn(("wan_ip", "198.51.100.1", "198.51.100.2"), changes)

    def test_disabled_trigger_is_not_reported(self) -> None:
        """A trigger explicitly disabled in config should never appear in the results."""
        notifications_config = {"notify_on": {"wan_change": False}}
        previous_network = {"external_ip": "203.0.113.10", "router": {"wan_ip": "198.51.100.1"}}
        current_network = {"external_ip": "203.0.113.10", "router": {"wan_ip": "198.51.100.2"}}

        changes = _detect_notifiable_changes(notifications_config, previous_network, current_network)

        self.assertEqual(changes, [])

    def test_missing_previous_value_does_not_count_as_a_change(self) -> None:
        """A field appearing for the first time (no prior value) should not fire a notification."""
        previous_network = {"external_ip": "203.0.113.10"}
        current_network = {"external_ip": "203.0.113.10", "router": {"wan_ip": "198.51.100.2"}}

        changes = _detect_notifiable_changes({}, previous_network, current_network)

        self.assertEqual(changes, [])


if __name__ == "__main__":
    unittest.main()