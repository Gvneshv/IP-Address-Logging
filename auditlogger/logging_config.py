"""Central logging configuration for AuditLogger.

Every module gets its logger the normal way (logging.getLogger(__name__)) and just logs - this module is the one place that decides where those records
end up (console, file, both) and at what level, driven by config.yaml's optional "logging" section.
"""

from __future__ import annotations
import logging
from pathlib import Path
from typing import Any


DEFAULT_LEVEL = "INFO"
DEFAULT_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def configure_logging(config: dict[str, Any]) -> None:
    """Configure the root logger from config["logging"] (all keys optional).

    Safe to call more than once per process - logging.basicConfig() is a no-op if the root logger already has handlers,
    so repeated calls (e.g. run_once() being invoked more than once by a long-lived caller) won't duplicate log lines.
    """
    logging_config = config.get("logging", {})
    level_name = str(logging_config.get("level", DEFAULT_LEVEL)).upper()
    level = getattr(logging, level_name, logging.INFO)

    handlers: list[logging.Handler] = [logging.StreamHandler()]

    log_file = logging_config.get("log_file")
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_path, encoding="utf-8"))

    logging.basicConfig(level=level, format=DEFAULT_FORMAT, handlers=handlers)