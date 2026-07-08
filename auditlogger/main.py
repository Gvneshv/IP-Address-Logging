"""Application entry points for collecting and writing one audit event."""

from __future__ import annotations
from pathlib import Path

from auditlogger.collector.network import collect_network_info
from auditlogger.collector.system import collect_system_info
from auditlogger.collector.timecheck import local_now_iso, utc_now_iso
from auditlogger.config.loader import load_config
from auditlogger.notifications.telegram import TelegramNotifier
from auditlogger.storage.hashchain import build_hashed_event
from auditlogger.storage.json_logger import JsonLogger


def build_event(config: dict) -> dict:
    """Build the unhashed audit event payload from current system state."""
    return {
        "timestamp_utc": utc_now_iso(),
        "timestamp_local": local_now_iso(),
        "network": collect_network_info(config["router"]),
        "system": collect_system_info(),
    }


def _detect_notifiable_changes(
    notifications_config: dict,
    previous_network: dict,
    current_network: dict,
) -> list[tuple[str, str, str]]:
    """Return (label, previous_value, current_value) for changes enabled in config.

    Each trigger defaults to enabled when notifications_config["notify_on"] omits it, preserving the pre-existing external-IP-only notification behaviour.
    A change only counts when both a previous and current value exist and differ - a field appearing for the first time
    (e.g. router data starting to populate once a real provider lands) is not treated as a "change".
    """
    notify_on = notifications_config.get("notify_on", {})
    changes: list[tuple[str, str, str]] = []

    if notify_on.get("external_ip_change", True):
        previous_ip = previous_network.get("external_ip")
        current_ip = current_network.get("external_ip")
        if previous_ip and current_ip and previous_ip != current_ip:
            changes.append(("external_ip", previous_ip, current_ip))

    if notify_on.get("wan_change", True):
        previous_wan = previous_network.get("router", {}).get("wan_ip")
        current_wan = current_network.get("router", {}).get("wan_ip")
        if previous_wan and current_wan and previous_wan != current_wan:
            changes.append(("wan_ip", previous_wan, current_wan))

    return changes


def run_once(config_path: str | Path | None = None) -> dict:
    """Collect, hash, persist, and optionally notify for a single audit event."""
    config = load_config(config_path)
    logger = JsonLogger(config["storage"]["log_file"])
    previous_event = logger.read_last_event()

    event = build_event(config)
    hashed_event = build_hashed_event(event, previous_event)
    logger.append(hashed_event)

    previous_network = (previous_event or {}).get("event", {}).get("network", {})
    changes = _detect_notifiable_changes(
        config.get("notifications", {}), previous_network, event["network"]
    )

    if changes:
        notifier = TelegramNotifier.from_config(config["telegram"])
        message_lines = ["AuditLogger: change detected"]
        message_lines += [f"{label}: {previous} -> {current}" for label, previous, current in changes]
        message_lines.append(f"Event hash: {hashed_event['hash']}")
        notifier.send_message("\n".join(message_lines))

    return hashed_event


def main() -> None:
    """Run the command-line entry point and print the stored event hash."""
    event = run_once()
    print(f"Audit event written: {event['hash']}")


if __name__ == "__main__":
    main()