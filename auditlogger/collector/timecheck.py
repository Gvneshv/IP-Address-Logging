"""Provide timestamp helpers used by audit event creation."""

from __future__ import annotations
import datetime as dt


def utc_now_iso() -> str:
    """Return the current UTC time as a second-precision ISO 8601 string."""
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def local_now_iso() -> str:
    """Return local time with the current system timezone offset."""
    return dt.datetime.now().astimezone().replace(microsecond=0).isoformat()
