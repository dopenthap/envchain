"""Access control: restrict which users/roles can activate a chain."""

from __future__ import annotations

import os
from typing import List

from envchain.storage import load_store, save_store


class AccessError(Exception):
    pass


def _access_key(chain: str) -> str:
    return f"__access__{chain}"


def set_access(store_path, chain: str, allowed: List[str]) -> None:
    """Set the list of allowed users for a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise AccessError(f"chain '{chain}' not found")
    if not allowed:
        raise AccessError("allowed list must not be empty")
    store[_access_key(chain)] = {"allowed": sorted(set(allowed))}
    save_store(store_path, store)


def remove_access(store_path, chain: str) -> None:
    """Remove access restrictions from a chain."""
    store = load_store(store_path)
    key = _access_key(chain)
    if key not in store:
        raise AccessError(f"no access rules set for chain '{chain}'")
    del store[key]
    save_store(store_path, store)


def get_access(store_path, chain: str) -> List[str] | None:
    """Return the allowed users list, or None if unrestricted."""
    store = load_store(store_path)
    key = _access_key(chain)
    if key not in store:
        return None
    return store[key]["allowed"]


def check_access(store_path, chain: str, user: str | None = None) -> bool:
    """Return True if the given user (default: current OS user) is allowed."""
    allowed = get_access(store_path, chain)
    if allowed is None:
        return True
    if user is None:
        user = os.environ.get("USER") or os.environ.get("USERNAME") or ""
    return user in allowed


def assert_access(store_path, chain: str, user: str | None = None) -> None:
    """Raise AccessError if the current user is not allowed."""
    if not check_access(store_path, chain, user):
        if user is None:
            user = os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"
        raise AccessError(f"user '{user}' is not allowed to access chain '{chain}'")
