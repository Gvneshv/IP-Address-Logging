"""Tests for the fallback YAML loader's nested-section parsing."""

from __future__ import annotations
import unittest

from auditlogger.config.loader import _load_simple_yaml


class LoaderNestingTests(unittest.TestCase):
    """Checks that the fallback parser supports the router config's depth."""

    def test_three_level_nesting_is_preserved(self) -> None:
        """router.connection.address should stay nested, not flatten to a string."""
        text = """
router:

  enabled: false

  connection:

      address:
      username:

  detection:

      type: auto
"""
        config = _load_simple_yaml(text)

        self.assertEqual(config["router"]["enabled"], False)
        self.assertIsInstance(config["router"]["connection"], dict)
        self.assertEqual(config["router"]["connection"]["address"], "")
        self.assertEqual(config["router"]["detection"]["type"], "auto")


if __name__ == "__main__":
    unittest.main()
