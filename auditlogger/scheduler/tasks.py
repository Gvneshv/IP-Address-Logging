"""Windows Task Scheduler helpers for installing AuditLogger startup runs."""

from __future__ import annotations
import subprocess
import sys
from pathlib import Path


def create_windows_startup_task(task_name: str = "AuditLogger") -> subprocess.CompletedProcess[str]:
    """Create or replace a limited-privilege task that runs at user logon."""
    command = f'"{sys.executable}" -m auditlogger.main'
    project_root = Path(__file__).resolve().parents[2]

    return subprocess.run(
        [
            "schtasks",
            "/Create",
            "/TN",
            task_name,
            "/SC",
            "ONLOGON",
            "/TR",
            command,
            "/RL",
            "LIMITED",
            "/F",
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
