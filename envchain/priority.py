"""Priority ordering for chains within a project."""

from __future__ import annotations

from envchain.storage import load_store, save_store

PRIORITY_KEY = "__priority__"


class PriorityError(Exception):
    pass


def _priority_key(chain: str) -> str:
    return f"{PRIORITY_KEY}:{chain}"


def set_priority(store_path, chain: str, priority: int) -> None:
    store = load_store(store_path)
    if chain not in store:
        raise PriorityError(f"chain '{chain}' not found")
    if not isinstance(priority, int) or priority < 0:
        raise PriorityError("priority must be a non-negative integer")
    meta = store.setdefault("__meta__", {})
    meta[_priority_key(chain)] = priority
    save_store(store_path, store)


def get_priority(store_path, chain: str) -> int | None:
    store = load_store(store_path)
    if chain not in store:
        raise PriorityError(f"chain '{chain}' not found")
    meta = store.get("__meta__", {})
    val = meta.get(_priority_key(chain))
    return int(val) if val is not None else None


def remove_priority(store_path, chain: str) -> None:
    store = load_store(store_path)
    if chain not in store:
        raise PriorityError(f"chain '{chain}' not found")
    meta = store.get("__meta__", {})
    key = _priority_key(chain)
    if key not in meta:
        raise PriorityError(f"chain '{chain}' has no priority set")
    del meta[key]
    save_store(store_path, store)


def list_by_priority(store_path) -> list[tuple[str, int | None]]:
    """Return all non-meta chains sorted by priority (None last)."""
    store = load_store(store_path)
    meta = store.get("__meta__", {})
    chains = [k for k in store if not k.startswith("__")]

    def sort_key(name: str):
        val = meta.get(_priority_key(name))
        if val is None:
            return (1, 0, name)
        return (0, int(val), name)

    chains.sort(key=sort_key)
    result = []
    for name in chains:
        val = meta.get(_priority_key(name))
        result.append((name, int(val) if val is not None else None))
    return result
