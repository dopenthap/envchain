"""Tier management for chains (e.g. free, dev, staging, prod)."""

from envchain.storage import load_store, save_store

VALID_TIERS = {"free", "dev", "staging", "prod"}


class TierError(Exception):
    pass


def _tier_key(chain: str) -> str:
    return f"__tier__{chain}"


def set_tier(store_path, chain: str, tier: str) -> None:
    """Assign a tier to a chain."""
    tier = tier.strip().lower()
    if tier not in VALID_TIERS:
        raise TierError(
            f"Invalid tier {tier!r}. Must be one of: {', '.join(sorted(VALID_TIERS))}"
        )
    store = load_store(store_path)
    if chain not in store:
        raise TierError(f"Chain {chain!r} not found.")
    store[_tier_key(chain)] = tier
    save_store(store_path, store)


def get_tier(store_path, chain: str) -> str | None:
    """Return the tier for a chain, or None if not set."""
    store = load_store(store_path)
    if chain not in store:
        raise TierError(f"Chain {chain!r} not found.")
    return store.get(_tier_key(chain))


def clear_tier(store_path, chain: str) -> None:
    """Remove the tier from a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise TierError(f"Chain {chain!r} not found.")
    key = _tier_key(chain)
    if key not in store:
        raise TierError(f"Chain {chain!r} has no tier set.")
    del store[key]
    save_store(store_path, store)


def list_tiers(store_path) -> dict[str, str]:
    """Return a mapping of chain name -> tier for all chains that have one."""
    store = load_store(store_path)
    prefix = "__tier__"
    return {
        k[len(prefix):]: v
        for k, v in store.items()
        if k.startswith(prefix)
    }
