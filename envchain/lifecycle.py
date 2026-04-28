"""Lifecycle hooks for chain activation and deactivation events.

Allows attaching shell commands to run when a chain is activated or
deactivated. Useful for setup/teardown tasks like starting services,
setting up virtualenvs, or notifying external systems.
"""

from __future__ import annotations

from typing import Optional

from .storage import load_store, save_store


class LifecycleError(Exception):
    pass


_ACTIVATE_KEY = "__lifecycle_activate__"
_DEACTIVATE_KEY = "__lifecycle_deactivate__"


def _activate_key(chain: str) -> str:
    return f"{chain}.{_ACTIVATE_KEY}"


def _deactivate_key(chain: str) -> str:
    return f"{chain}.{_DEACTIVATE_KEY}"


def set_hook(chain: str, event: str, command: str, store_path=None) -> None:
    """Attach a shell command to a lifecycle event for the given chain.

    Args:
        chain: Name of the chain.
        event: Either 'activate' or 'deactivate'.
        command: Shell command string to run on the event.
        store_path: Optional path override for the store file.
    """
    if event not in ("activate", "deactivate"):
        raise LifecycleError(f"Unknown lifecycle event: {event!r}. Use 'activate' or 'deactivate'.")

    store = load_store(store_path)
    if chain not in store:
        raise LifecycleError(f"Chain not found: {chain!r}")

    meta_key = _activate_key(chain) if event == "activate" else _deactivate_key(chain)
    store[meta_key] = command
    save_store(store, store_path)


def remove_hook(chain: str, event: str, store_path=None) -> None:
    """Remove a lifecycle hook from the given chain.

    Args:
        chain: Name of the chain.
        event: Either 'activate' or 'deactivate'.
        store_path: Optional path override for the store file.
    """
    if event not in ("activate", "deactivate"):
        raise LifecycleError(f"Unknown lifecycle event: {event!r}. Use 'activate' or 'deactivate'.")

    store = load_store(store_path)
    if chain not in store:
        raise LifecycleError(f"Chain not found: {chain!r}")

    meta_key = _activate_key(chain) if event == "activate" else _deactivate_key(chain)
    if meta_key not in store:
        raise LifecycleError(f"No {event!r} hook set for chain {chain!r}")

    del store[meta_key]
    save_store(store, store_path)


def get_hook(chain: str, event: str, store_path=None) -> Optional[str]:
    """Return the shell command for the given lifecycle event, or None.

    Args:
        chain: Name of the chain.
        event: Either 'activate' or 'deactivate'.
        store_path: Optional path override for the store file.
    """
    if event not in ("activate", "deactivate"):
        raise LifecycleError(f"Unknown lifecycle event: {event!r}. Use 'activate' or 'deactivate'.")

    store = load_store(store_path)
    if chain not in store:
        raise LifecycleError(f"Chain not found: {chain!r}")

    meta_key = _activate_key(chain) if event == "activate" else _deactivate_key(chain)
    return store.get(meta_key)


def list_hooks(store_path=None) -> dict[str, dict[str, str]]:
    """Return all lifecycle hooks across all chains.

    Returns a dict mapping chain name to a dict with optional keys
    'activate' and 'deactivate'.

    Args:
        store_path: Optional path override for the store file.
    """
    store = load_store(store_path)
    result: dict[str, dict[str, str]] = {}

    for key, value in store.items():
        if key.endswith(f".{_ACTIVATE_KEY}"):
            chain = key[: -len(f".{_ACTIVATE_KEY}")]
            result.setdefault(chain, {})["activate"] = value
        elif key.endswith(f".{_DEACTIVATE_KEY}"):
            chain = key[: -len(f".{_DEACTIVATE_KEY}")]
            result.setdefault(chain, {})["deactivate"] = value

    return result
