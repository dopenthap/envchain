"""protect.py — mark chains as read-only to prevent accidental modification."""

from envchain.storage import load_store, save_store

PROTECT_KEY = "__protected__"


class ProtectError(Exception):
    pass


def protect_chain(chain: str, store_path) -> None:
    """Mark a chain as protected (read-only)."""
    store = load_store(store_path)
    if chain not in store:
        raise ProtectError(f"chain '{chain}' not found")
    store.setdefault("__meta__", {})
    store["__meta__"].setdefault(chain, {})
    store["__meta__"][chain][PROTECT_KEY] = True
    save_store(store_path, store)


def unprotect_chain(chain: str, store_path) -> None:
    """Remove protection from a chain."""
    store = load_store(store_path)
    meta = store.get("__meta__", {}).get(chain, {})
    if not meta.get(PROTECT_KEY):
        raise ProtectError(f"chain '{chain}' is not protected")
    store["__meta__"][chain].pop(PROTECT_KEY)
    save_store(store_path, store)


def is_protected(chain: str, store_path) -> bool:
    """Return True if the chain is currently protected."""
    store = load_store(store_path)
    return bool(store.get("__meta__", {}).get(chain, {}).get(PROTECT_KEY))


def assert_unprotected(chain: str, store_path) -> None:
    """Raise ProtectError if the chain is protected."""
    if is_protected(chain, store_path):
        raise ProtectError(f"chain '{chain}' is protected; unprotect it first")


def list_protected(store_path) -> list[str]:
    """Return sorted list of all protected chain names."""
    store = load_store(store_path)
    return sorted(
        chain
        for chain, meta in store.get("__meta__", {}).items()
        if meta.get(PROTECT_KEY)
    )
