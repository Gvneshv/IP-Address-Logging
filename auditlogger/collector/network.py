"""Collect external and local network identity for audit events."""

from __future__ import annotations

import socket
import subprocess
import urllib.error
import urllib.request

from .router import collect_router_info


def get_external_ip(timeout_seconds: float = 5.0) -> str | None:
    """Return the public IPv4 address reported by the first reachable endpoint."""
    endpoints = (
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
    )

    for endpoint in endpoints:
        try:
            with urllib.request.urlopen(endpoint, timeout=timeout_seconds) as response:
                value = response.read().decode("utf-8").strip()
                if value:
                    return value
        except (urllib.error.URLError, TimeoutError, OSError):
            continue

    return None


def get_local_ip() -> str | None:
    """Return the local IPv4 address Windows would use for outbound traffic."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return None


def _parse_ipconfig_adapter(output: str, local_ip: str) -> dict | None:
    """Return the adapter section from ipconfig output that owns local_ip."""
    current_name = None
    current_fields = {}

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if line.endswith(":") and " adapter " in line:
            match = _adapter_from_ipconfig_section(current_name, current_fields, local_ip)
            if match:
                return match

            current_name = line.rsplit(" adapter ", 1)[1][:-1]
            current_fields = {}
            continue

        if current_name and ":" in line:
            key, value = line.split(":", 1)
            normalized_key = key.replace(".", "").strip().lower()
            current_fields[normalized_key] = value.strip()

    return _adapter_from_ipconfig_section(current_name, current_fields, local_ip)


def _adapter_from_ipconfig_section(
    adapter_name: str | None,
    fields: dict[str, str],
    local_ip: str,
) -> dict | None:
    """Build adapter metadata when an ipconfig section contains local_ip."""
    if not adapter_name:
        return None

    has_local_ip = any(local_ip in value for value in fields.values())
    if not has_local_ip:
        return None

    return {
        "adapter_name": adapter_name,
        "mac": fields.get("physical address"),
    }


def get_windows_adapter_for_ip(local_ip: str | None) -> dict | None:
    """Return the Windows adapter name and MAC address for a local IPv4 address."""
    if not local_ip:
        return None

    try:
        result = subprocess.run(
            ["ipconfig", "/all"],
            capture_output=True,
            check=False,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    if result.returncode != 0 or not result.stdout.strip():
        return None

    return _parse_ipconfig_adapter(result.stdout, local_ip)


def collect_network_info(router_config: dict) -> dict:
    """Collect the network fields written into an audit event.

    router_config is the "router" section of the app config (main.py passes config["router"] in),
    not the full config - the parameter name reflects that so it isn't mistaken for the whole app config further down.
    """
    local_ip = get_local_ip()
    adapter = get_windows_adapter_for_ip(local_ip) or {}
    router_info = collect_router_info(router_config)
    result = {
        "external_ip": get_external_ip(),
        "local_ip": local_ip,
        "adapter_name": adapter.get("adapter_name"),
        "mac": adapter.get("mac"),
    }
    if router_info:
        result["router"] = router_info

    return result
