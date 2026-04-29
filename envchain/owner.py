"""Chain ownership metadata — assign an owner string to a chain."""

from __future__ import annotations

from envchain.storage import load_store, save_store


class OwnerError(Exception):
    pass


def _owner_key(chain: str) -> str:
    return f"__meta__:owner:{chain}"


def set_owner(chain: str, owner: str, *, store_path) -> None:
    """Assign an owner to *chain*."""
    store = load_store(store_path)
    if chain not in store:
        raise OwnerError(f"chain '{chain}' not found")
    owner = owner.strip()
    if not owner:
        raise OwnerError("owner must not be empty")
    store[_owner_key(chain)] = {"_owner": owner}
    save_store(store_path, store)


def get_owner(chain: str, *, store_path) -> str | None:
    """Return the owner of *chain*, or None if unset."""
    store = load_store(store_path)
    if chain not in store:
        raise OwnerError(f"chain '{chain}' not found")
    meta = store.get(_owner_key(chain), {})
    return meta.get("_owner")


def clear_owner(chain: str, *, store_path) -> None:
    """Remove the owner entry for *chain*."""
    store = load_store(store_path)
    if chain not in store:
        raise OwnerError(f"chain '{chain}' not found")
    store.pop(_owner_key(chain), None)
    save_store(store_path, store)


def list_owners(*, store_path) -> dict[str, str]:
    """Return a mapping of chain_name -> owner for all chains that have one."""
    store = load_store(store_path)
    result: dict[str, str] = {}
    prefix = "__meta__:owner:"
    for key, val in store.items():
        if key.startswith(prefix):
            chain = key[len(prefix):]
            owner = val.get("_owner")
            if owner:
                result[chain] = owner
    return result
