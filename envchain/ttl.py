"""TTL (time-to-live) support for chains — auto-expire after a duration."""

from __future__ import annotations

import time
from typing import Optional

from envchain.storage import load_store, save_store


class TtlError(Exception):
    pass


def _ttl_key(chain: str) -> str:
    return f"__ttl__{chain}"


def set_ttl(store_path, chain: str, seconds: int) -> None:
    """Set a TTL for a chain. Stores the absolute expiry timestamp."""
    store = load_store(store_path)
    if chain not in store:
        raise TtlError(f"chain '{chain}' not found")
    if seconds <= 0:
        raise TtlError("TTL must be a positive number of seconds")
    expires_at = time.time() + seconds
    store[_ttl_key(chain)] = {"expires_at": expires_at, "seconds": seconds}
    save_store(store_path, store)


def remove_ttl(store_path, chain: str) -> None:
    """Remove the TTL for a chain."""
    store = load_store(store_path)
    key = _ttl_key(chain)
    if key not in store:
        raise TtlError(f"no TTL set for chain '{chain}'")
    del store[key]
    save_store(store_path, store)


def get_ttl(store_path, chain: str) -> Optional[dict]:
    """Return TTL info dict or None if not set."""
    store = load_store(store_path)
    if chain not in store:
        raise TtlError(f"chain '{chain}' not found")
    return store.get(_ttl_key(chain))


def is_expired(store_path, chain: str) -> bool:
    """Return True if the chain's TTL has elapsed."""
    info = get_ttl(store_path, chain)
    if info is None:
        return False
    return time.time() > info["expires_at"]


def list_ttls(store_path) -> dict:
    """Return mapping of chain name -> TTL info for all chains that have a TTL."""
    store = load_store(store_path)
    prefix = "__ttl__"
    result = {}
    for key, value in store.items():
        if key.startswith(prefix):
            chain = key[len(prefix):]
            result[chain] = value
    return result
