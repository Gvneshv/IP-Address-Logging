"""Append and read newline-delimited JSON audit events."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Iterable


class JsonLogger:
    """Persist audit events in a JSONL file on local disk."""

    def __init__(self, log_file: str | Path) -> None:
        """Create a logger for log_file and ensure its parent directory exists."""
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: dict) -> None:
        """Append one JSON-serializable event to the log file."""
        with self.log_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, ensure_ascii=False, sort_keys=True))
            file.write("\n")

    def read_events(self) -> Iterable[dict]:
        """Read all stored events in file order."""
        if not self.log_file.exists():
            return []

        events = []
        with self.log_file.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return events

    def read_last_event(self) -> dict | None:
        """Return the most recently stored event, or None for an empty log."""
        events = list(self.read_events())
        return events[-1] if events else None
