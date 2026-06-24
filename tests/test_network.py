"""Tests for Windows network adapter parsing."""

from __future__ import annotations
import unittest

from auditlogger.collector.network import _parse_ipconfig_adapter


class NetworkTests(unittest.TestCase):
    """Checks for mapping selected local IP addresses to adapter metadata."""

    def test_parse_ipconfig_adapter_for_selected_local_ip(self) -> None:
        """The parser should select the adapter section owning the local IP."""
        output = """
Windows IP Configuration

Ethernet adapter Supreme Wired:

   Description . . . . . . . . . . . : Intel(R) Ethernet Connection (7) I219-V
   Physical Address. . . . . . . . . : 00-D8-61-A6-80-3C
   IPv4 Address. . . . . . . . . . . : 192.168.0.130(Preferred)

Ethernet adapter Ethernet 3:

   Physical Address. . . . . . . . . : 0A-00-27-00-00-08
   IPv4 Address. . . . . . . . . . . : 192.168.56.1(Preferred)
"""

        adapter = _parse_ipconfig_adapter(output, "192.168.0.130")

        self.assertEqual(
            adapter,
            {
                "adapter_name": "Supreme Wired",
                "mac": "00-D8-61-A6-80-3C",
            },
        )


if __name__ == "__main__":
    unittest.main()
