"""Region/environment tagging for chains (e.g. dev, staging, prod)."""

from __future__ import annotations

from envchain.storage import load_store, save_store

REGION_KEY_PREFIX = "__region__"
VALID_REGIONS = {"dev", "staging", "prod", "local", "test"}


class RegionError(Exception):
    pass


def _region_key(chain: str) -> str:
    return f"{REGION_KEY_PREFIX}{chain}"


def set_region(store_path, chain: str, region: str) -> None:
    """Assign a region to a chain."""
    if region not in VALID_REGIONS:
        raise RegionError(
            f"Invalid region '{region}'. Valid regions: {sorted(VALID_REGIONS)}"
        )
    store = load_store(store_path)
    if chain not in store:
        raise RegionError(f"Chain '{chain}' not found.")
    store[_region_key(chain)] = region
    save_store(store_path, store)


def get_region(store_path, chain: str) -> str | None:
    """Return the region assigned to a chain, or None if unset."""
    store = load_store(store_path)
    if chain not in store:
        raise RegionError(f"Chain '{chain}' not found.")
    return store.get(_region_key(chain))


def clear_region(store_path, chain: str) -> None:
    """Remove the region assignment from a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise RegionError(f"Chain '{chain}' not found.")
    key = _region_key(chain)
    if key not in store:
        raise RegionError(f"Chain '{chain}' has no region set.")
    del store[key]
    save_store(store_path, store)


def list_by_region(store_path, region: str) -> list[str]:
    """Return all chain names assigned to the given region."""
    if region not in VALID_REGIONS:
        raise RegionError(
            f"Invalid region '{region}'. Valid regions: {sorted(VALID_REGIONS)}"
        )
    store = load_store(store_path)
    return sorted(
        chain
        for chain, value in store.items()
        if not chain.startswith("__")
        and store.get(_region_key(chain)) == region
    )
