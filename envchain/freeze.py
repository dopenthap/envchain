"""Freeze/unfreeze chains to prevent any modifications."""

from envchain.storage import load_store, save_store

FREEZE_PREFIX = "__frozen__"


class FreezeError(Exception):
    pass


def _freeze_key(chain: str) -> str:
    return f"{FREEZE_PREFIX}{chain}"


def freeze_chain(chain: str, store_path) -> None:
    """Mark a chain as frozen, preventing any modifications."""
    store = load_store(store_path)
    if chain not in store:
        raise FreezeError(f"Chain '{chain}' not found.")
    if is_frozen(chain, store_path):
        raise FreezeError(f"Chain '{chain}' is already frozen.")
    store[_freeze_key(chain)] = "1"
    save_store(store_path, store)


def unfreeze_chain(chain: str, store_path) -> None:
    """Remove the frozen mark from a chain."""
    store = load_store(store_path)
    key = _freeze_key(chain)
    if key not in store:
        raise FreezeError(f"Chain '{chain}' is not frozen.")
    del store[key]
    save_store(store_path, store)


def is_frozen(chain: str, store_path) -> bool:
    """Return True if the chain is currently frozen."""
    store = load_store(store_path)
    return _freeze_key(chain) in store


def assert_unfrozen(chain: str, store_path) -> None:
    """Raise FreezeError if the chain is frozen."""
    if is_frozen(chain, store_path):
        raise FreezeError(f"Chain '{chain}' is frozen and cannot be modified.")


def list_frozen(store_path) -> list[str]:
    """Return a sorted list of all frozen chain names."""
    store = load_store(store_path)
    prefix = FREEZE_PREFIX
    return sorted(
        key[len(prefix):]
        for key in store
        if key.startswith(prefix)
    )
