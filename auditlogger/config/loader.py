"""Load AuditLogger configuration with a small YAML fallback parser."""

from __future__ import annotations
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = Path(__file__).with_name("config.yaml")


def _parse_scalar(value: str) -> Any:
    """Parse the scalar values supported by the fallback YAML loader."""
    value = value.strip()

    if value in {"true", "false"}:
        return value == "true"
    if value == "[]":
        return []
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def _load_simple_yaml(text: str) -> dict[str, Any]:
    """Load the simple section/key YAML shape used by the example config."""
    result: dict[str, Any] = {}
    current_section: dict[str, Any] | None = None

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        if not raw_line.startswith(" ") and line.endswith(":"):
            section_name = line[:-1].strip()
            current_section = {}
            result[section_name] = current_section
            continue

        if current_section is not None and raw_line.startswith("  ") and ":" in line:
            key, value = line.split(":", 1)
            current_section[key.strip()] = _parse_scalar(value)
            continue

        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = _parse_scalar(value)

    return result


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load configuration from config_path or the package config.yaml file."""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH

    if not path.exists():
        example = path.with_name("config.example.yaml")
        raise FileNotFoundError(
            f"Config file not found: {path}. Copy {example.name} to {path.name} and adjust values."
        )

    text = path.read_text(encoding="utf-8")

    try:
        import yaml
    except ModuleNotFoundError:
        return _load_simple_yaml(text)

    return yaml.safe_load(text) or {}
