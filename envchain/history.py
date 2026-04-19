"""Track which chain was last activated per project directory."""

from __future__ import annotations

import json
from pathlib import Path


def get_history_path() -> Path:
    base = Path.home() / ".config" / "envchain"
    return base / "history.json"


def load_history(history_path: Path | None = None) -> dict:
    path = history_path or get_history_path()
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)


def save_history(data: dict, history_path: Path | None = None) -> None:
    path = history_path or get_history_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def record_activation(project: str, chain: str, history_path: Path | None = None) -> None:
    """Record that `chain` was last activated for `project`."""
    data = load_history(history_path)
    data[project] = chain
    save_history(data, history_path)


def get_last_chain(project: str, history_path: Path | None = None) -> str | None:
    """Return the last activated chain for `project`, or None."""
    data = load_history(history_path)
    return data.get(project)


def list_history(history_path: Path | None = None) -> dict:
    """Return all recorded project -> chain mappings."""
    return load_history(history_path)
