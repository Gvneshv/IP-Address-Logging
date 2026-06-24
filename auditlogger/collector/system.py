"""Collect host and operating-system details for audit events."""

from __future__ import annotations
import ctypes
import datetime as dt
import platform
import socket


def get_boot_time_utc() -> str | None:
    """Return Windows boot time in UTC, or None when unavailable."""
    if platform.system().lower() != "windows":
        return None

    try:
        uptime_ms = ctypes.windll.kernel32.GetTickCount64()
    except AttributeError:
        return None

    boot_time = dt.datetime.now(dt.UTC) - dt.timedelta(milliseconds=uptime_ms)
    return boot_time.replace(microsecond=0).isoformat()


def collect_system_info() -> dict:
    """Collect hostname, platform, and boot-time fields for the audit log."""
    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "boot_time_utc": get_boot_time_utc(),
    }
