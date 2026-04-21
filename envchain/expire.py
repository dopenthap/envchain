"""Chain expiry: set a TTL on a chain and check if it has expired."""

from __future__ import annotations

import datetime
from typing import Optional

from envchain.storage import load_store, save_store


class ExpireError(Exception):
    pass


def _expire_key(chain: str) -> str:
    return f"__expire__{chain}"


def set_expiry(store_path, chain: str, expires_at: datetime.datetime) -> None:
    """Set an expiry datetime (UTC) for a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise ExpireError(f"chain '{chain}' not found")
    store[_expire_key(chain)] = expires_at.isoformat()
    save_store(store_path, store)


def remove_expiry(store_path, chain: str) -> None:
    """Remove expiry from a chain. Raises if no expiry is set."""
    store = load_store(store_path)
    key = _expire_key(chain)
    if key not in store:
        raise ExpireError(f"chain '{chain}' has no expiry set")
    del store[key]
    save_store(store_path, store)


def get_expiry(store_path, chain: str) -> Optional[datetime.datetime]:
    """Return the expiry datetime for a chain, or None if not set."""
    store = load_store(store_path)
    if chain not in store:
        raise ExpireError(f"chain '{chain}' not found")
    key = _expire_key(chain)
    if key not in store:
        return None
    return datetime.datetime.fromisoformat(store[key])


def is_expired(store_path, chain: str) -> bool:
    """Return True if the chain has an expiry that is in the past."""
    expiry = get_expiry(store_path, chain)
    if expiry is None:
        return False
    return datetime.datetime.utcnow() > expiry


def list_expiries(store_path) -> dict[str, datetime.datetime]:
    """Return a mapping of chain name -> expiry datetime for all chains with expiry set."""
    store = load_store(store_path)
    result = {}
    prefix = "__expire__"
    for key, value in store.items():
        if key.startswith(prefix):
            chain = key[len(prefix):]
            result[chain] = datetime.datetime.fromisoformat(value)
    return result
