"""Hash audit event payloads into deterministic tamper-evident records."""

from __future__ import annotations
import hashlib
import json


def canonical_json(data: dict) -> str:
    """Serialize data in the stable form used for event hashing."""
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_hex(data: str) -> str:
    """Return the SHA256 hex digest for a UTF-8 string."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def build_hashed_event(event: dict, previous_event: dict | None = None) -> dict:
    """Wrap an event with the previous hash and its own SHA256 digest."""
    previous_hash = (previous_event or {}).get("hash")
    payload = {
        "event": event,
        "previous_hash": previous_hash,
    }

    return {
        **payload,
        "hash": sha256_hex(canonical_json(payload)),
    }


def verify_event_hash(stored_event: dict) -> bool:
    """Return whether a stored event still matches its recorded hash."""
    payload = {
        "event": stored_event.get("event"),
        "previous_hash": stored_event.get("previous_hash"),
    }
    return stored_event.get("hash") == sha256_hex(canonical_json(payload))
