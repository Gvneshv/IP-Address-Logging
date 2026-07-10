"""Send audit notifications through Telegram when configured."""

from __future__ import annotations
import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TelegramNotifier:
    """Small Telegram Bot API client controlled by project configuration."""

    bot_token: str | None
    chat_id: str | None
    enabled: bool = False

    @classmethod
    def from_config(cls, config: dict) -> "TelegramNotifier":
        """Create a notifier from the telegram section of the config file."""
        return cls(
            bot_token=config.get("bot_token"),
            chat_id=config.get("chat_id"),
            enabled=bool(config.get("enabled")),
        )

    def send_message(self, text: str) -> bool:
        """Send text to the configured chat and report whether Telegram accepted it."""
        if not self.enabled or not self.bot_token or not self.chat_id:
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": self.chat_id, "text": text}).encode("utf-8")
        request = urllib.request.Request(url, data=data, method="POST")

        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                payload = json.loads(response.read().decode("utf-8"))
                return bool(payload.get("ok"))
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
            logger.warning("Telegram notification failed: %s", error)
            return False