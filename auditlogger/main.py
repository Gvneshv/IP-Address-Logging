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


def run_once(config_path: str | Path | None = None) -> dict:
    """Collect, hash, persist, and optionally notify for a single audit event."""
    config = load_config(config_path)
    logger = JsonLogger(config["storage"]["log_file"])
    previous_event = logger.read_last_event()

    event = build_event(config)
    hashed_event = build_hashed_event(event, previous_event)
    logger.append(hashed_event)

    previous_ip = (previous_event or {}).get("event", {}).get("network", {}).get("external_ip")
    current_ip = event["network"].get("external_ip")

    if current_ip and previous_ip and current_ip != previous_ip:
        notifier = TelegramNotifier.from_config(config["telegram"])
        notifier.send_message(
            "AuditLogger: external IP changed\n"
            f"Previous: {previous_ip}\n"
            f"Current: {current_ip}\n"
            f"Event hash: {hashed_event['hash']}"
        )

    return hashed_event


def main() -> None:
    """Run the command-line entry point and print the stored event hash."""
    event = run_once()
    print(f"Audit event written: {event['hash']}")


if __name__ == "__main__":
    main()
