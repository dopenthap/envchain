"""Audit log for envchain operations."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

APP_DIR = Path.home() / ".config" / "envchain"
AUDIT_FILE = APP_DIR / "audit.log"


def get_audit_path(base: Path | None = None) -> Path:
    if base is not None:
        return base / "audit.log"
    return AUDIT_FILE


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def record_event(action: str, chain: str, detail: str = "", audit_path: Path | None = None) -> None:
    path = get_audit_path(audit_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {"ts": _now_iso(), "action": action, "chain": chain, "detail": detail}
    with path.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def load_events(audit_path: Path | None = None) -> list[dict]:
    path = get_audit_path(audit_path)
    if not path.exists():
        return []
    events = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events


def clear_events(audit_path: Path | None = None) -> None:
    path = get_audit_path(audit_path)
    if path.exists():
        path.write_text("")
