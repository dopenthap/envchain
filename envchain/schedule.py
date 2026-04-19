"""Schedule-based chain activation reminders."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Optional


class ScheduleError(Exception):
    pass


def _schedule_path(base: Optional[Path] = None) -> Path:
    if base is None:
        base = Path.home() / ".config" / "envchain"
    return base / "schedules.json"


def load_schedules(base: Optional[Path] = None) -> dict:
    p = _schedule_path(base)
    if not p.exists():
        return {}
    return json.loads(p.read_text())


def save_schedules(data: dict, base: Optional[Path] = None) -> None:
    p = _schedule_path(base)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2))


def set_schedule(chain: str, cron: str, message: str = "", base: Optional[Path] = None) -> None:
    data = load_schedules(base)
    data[chain] = {"cron": cron, "message": message}
    save_schedules(data, base)


def remove_schedule(chain: str, base: Optional[Path] = None) -> None:
    data = load_schedules(base)
    if chain not in data:
        raise ScheduleError(f"No schedule for chain '{chain}'")
    del data[chain]
    save_schedules(data, base)


def get_schedule(chain: str, base: Optional[Path] = None) -> dict:
    data = load_schedules(base)
    if chain not in data:
        raise ScheduleError(f"No schedule for chain '{chain}'")
    return data[chain]


def list_schedules(base: Optional[Path] = None) -> dict:
    return load_schedules(base)
