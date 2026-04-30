from __future__ import annotations

from envchain.storage import load_store, save_store

VERSION_KEY_PREFIX = "__version__:"


class VersionError(Exception):
    pass


def _version_key(chain: str) -> str:
    return f"{VERSION_KEY_PREFIX}{chain}"


def bump_version(store_path, chain: str) -> int:
    """Increment the version counter for a chain and return the new version."""
    store = load_store(store_path)
    if chain not in store:
        raise VersionError(f"chain '{chain}' not found")
    key = _version_key(chain)
    current = int(store.get(key, 0))
    new_version = current + 1
    store[key] = new_version
    save_store(store_path, store)
    return new_version


def get_version(store_path, chain: str) -> int:
    """Return the current version number for a chain (0 if never bumped)."""
    store = load_store(store_path)
    if chain not in store:
        raise VersionError(f"chain '{chain}' not found")
    key = _version_key(chain)
    return int(store.get(key, 0))


def reset_version(store_path, chain: str) -> None:
    """Reset the version counter for a chain back to 0."""
    store = load_store(store_path)
    if chain not in store:
        raise VersionError(f"chain '{chain}' not found")
    key = _version_key(chain)
    store.pop(key, None)
    save_store(store_path, store)


def list_versions(store_path) -> dict[str, int]:
    """Return a mapping of chain name -> version for all chains that have a version set."""
    store = load_store(store_path)
    result = {}
    for key, val in store.items():
        if key.startswith(VERSION_KEY_PREFIX):
            chain = key[len(VERSION_KEY_PREFIX):]
            result[chain] = int(val)
    return result
