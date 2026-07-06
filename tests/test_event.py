"""Tests for event assembly and timestamp behavior."""

from __future__ import annotations
import datetime as dt
import unittest
from unittest.mock import patch

from auditlogger.collector.timecheck import local_now_iso
from auditlogger.main import build_event


class EventTests(unittest.TestCase):
    """Checks for the audit event shape produced by main.build_event."""

    def test_local_timestamp_has_timezone_offset(self) -> None:
        """Local timestamps should carry the current system timezone offset."""
        timestamp = dt.datetime.fromisoformat(local_now_iso())

        self.assertIsNotNone(timestamp.tzinfo)
        self.assertIsNotNone(timestamp.utcoffset())

    @patch("auditlogger.main.collect_system_info", return_value={"hostname": "host"})
    @patch(
        "auditlogger.main.collect_network_info",
        return_value={
            "external_ip": "203.0.113.10",
            "local_ip": "192.168.0.130",
            "adapter_name": "Supreme Wired",
            "mac": "00-D8-61-A6-80-3C",
        },
    )
    def test_event_includes_local_timestamp_and_adapter_fields(
        self,
        _collect_network_info,
        _collect_system_info,
    ) -> None:
        """Events should expose both local time and adapter-specific MAC data."""
        event = build_event(
            {
                "router": {}
            })

        self.assertIn("timestamp_utc", event)
        self.assertIn("timestamp_local", event)
        self.assertEqual(event["network"]["adapter_name"], "Supreme Wired")
        self.assertEqual(event["network"]["mac"], "00-D8-61-A6-80-3C")


if __name__ == "__main__":
    unittest.main()
