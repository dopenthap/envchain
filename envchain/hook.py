"""Pre/post activation hooks for chains."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from envchain.storage import load_store, save_store, get_store_path


class HookError(Exception):
    pass


HOOK_EVENTS = ("pre_activate", "post_activate", "pre_deactivate", "post_deactivate")


def _hook_key(chain: str, event: str) -> str:
    return f"__hook__{chain}__{event}"


def set_hook(chain: str, event: str, command: str, store_path: Optional[Path] = None) -> None:
    if event not in HOOK_EVENTS:
        raise HookError(f"Unknown event '{event}'. Valid events: {', '.join(HOOK_EVENTS)}")
    store = load_store(store_path)
    if chain not in store:
        raise HookError(f"Chain '{chain}' not found")
    store[_hook_key(chain, event)] = {"command": command}
    save_store(store, store_path)


def remove_hook(chain: str, event: str, store_path: Optional[Path] = None) -> None:
    if event not in HOOK_EVENTS:
        raise HookError(f"Unknown event '{event}'. Valid events: {', '.join(HOOK_EVENTS)}")
    store = load_store(store_path)
    key = _hook_key(chain, event)
    if key not in store:
        raise HookError(f"No hook set for '{chain}' on event '{event}'")
    del store[key]
    save_store(store, store_path)


def get_hook(chain: str, event: str, store_path: Optional[Path] = None) -> Optional[str]:
    store = load_store(store_path)
    entry = store.get(_hook_key(chain, event))
    if entry is None:
        return None
    return entry.get("command")


def list_hooks(chain: str, store_path: Optional[Path] = None) -> dict[str, str]:
    store = load_store(store_path)
    if chain not in store:
        raise HookError(f"Chain '{chain}' not found")
    result = {}
    for event in HOOK_EVENTS:
        entry = store.get(_hook_key(chain, event))
        if entry is not None:
            result[event] = entry["command"]
    return result
