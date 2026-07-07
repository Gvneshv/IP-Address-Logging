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


def _indent_of(raw_line: str) -> int:
    """Return the number of leading spaces on a config line."""
    return len(raw_line) - len(raw_line.lstrip(" "))


def _load_simple_yaml(text: str) -> dict[str, Any]:
    """Load the indentation-nested section/key YAML shape used by the config.

    Supports arbitrary nesting depth (e.g. router -> connection -> address), which the config now requires.
    A "key:" line with nothing after the colon is treated as the start of a nested section only when the next non-blank line is indented further;
    otherwise it's an empty scalar (matches how a genuinely blank value like "address:" should behave).
    This is still a deliberately minimal parser - no lists of mappings, multi-line strings, or other full-YAML features are supported.
    Prefer installing PyYAML for anything beyond this project's own config shape.
    """
    lines: list[tuple[int, str]] = []
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if line.strip():
            lines.append((_indent_of(raw_line), line.strip()))

    root: dict[str, Any] = {}
    # Stack of (indent_level, dict_at_that_level); root sits below indent 0.
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]

    for index, (indent, key_part) in enumerate(lines):
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]

        if ":" not in key_part:
            continue

        key, _, value = key_part.partition(":")
        key = key.strip()
        value = value.strip()

        next_indent = lines[index + 1][0] if index + 1 < len(lines) else -1
        if not value and next_indent > indent:
            new_section: dict[str, Any] = {}
            parent[key] = new_section
            stack.append((indent, new_section))
        else:
            parent[key] = _parse_scalar(value)

    return root


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
