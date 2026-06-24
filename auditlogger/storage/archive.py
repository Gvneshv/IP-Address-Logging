"""Archive hooks reserved for the v2 storage workflow."""

from __future__ import annotations
from pathlib import Path


def daily_archive_placeholder(log_file: str | Path) -> Path:
    """v2 placeholder: archive current log into a date-based immutable bundle."""
    return Path(log_file)
