"""Notification hooks for chain activation events."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

NOTIFY_KEY = "__notify__"


class NotifyError(Exception):
    pass


def _notify_key(chain: str) -> str:
    return f"{NOTIFY_KEY}{chain}"


def set_notify(store: dict, chain: str, event: str, command: str) -> None:
    """Register a shell command to run when *event* fires for *chain*.

    Supported events: 'activate', 'deactivate'.
    """
    if event not in ("activate", "deactivate"):
        raise NotifyError(f"Unknown event '{event}'. Use 'activate' or 'deactivate'.")
    if chain not in store:
        raise NotifyError(f"Chain '{chain}' not found.")
    key = _notify_key(chain)
    hooks: dict[str, Any] = json.loads(store.get(key, "{}"))
    hooks[event] = command
    store[key] = json.dumps(hooks)


def remove_notify(store: dict, chain: str, event: str) -> None:
    """Remove the hook for *event* on *chain*."""
    if event not in ("activate", "deactivate"):
        raise NotifyError(f"Unknown event '{event}'. Use 'activate' or 'deactivate'.")
    key = _notify_key(chain)
    hooks: dict[str, Any] = json.loads(store.get(key, "{}"))
    if event not in hooks:
        raise NotifyError(f"No '{event}' hook set for chain '{chain}'.")
    del hooks[event]
    if hooks:
        store[key] = json.dumps(hooks)
    else:
        store.pop(key, None)


def get_notify(store: dict, chain: str, event: str) -> str | None:
    """Return the command registered for *event* on *chain*, or None."""
    key = _notify_key(chain)
    hooks: dict[str, Any] = json.loads(store.get(key, "{}"))
    return hooks.get(event)


def list_notify(store: dict, chain: str) -> dict[str, str]:
    """Return all hooks for *chain* as {event: command}."""
    key = _notify_key(chain)
    return json.loads(store.get(key, "{}"))
