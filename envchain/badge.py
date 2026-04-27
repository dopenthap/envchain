"""Badge feature: attach a short display badge/status string to a chain."""

from envchain.storage import load_store, save_store


class BadgeError(Exception):
    pass


def _badge_key(chain: str) -> str:
    return f"__badge__{chain}"


def set_badge(store_path, chain: str, badge: str) -> None:
    """Attach a badge string to a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise BadgeError(f"chain '{chain}' not found")
    if not badge or not badge.strip():
        raise BadgeError("badge must not be empty")
    if len(badge) > 32:
        raise BadgeError("badge must be 32 characters or fewer")
    store[_badge_key(chain)] = {"value": badge.strip()}
    save_store(store_path, store)


def get_badge(store_path, chain: str) -> str | None:
    """Return the badge for a chain, or None if not set."""
    store = load_store(store_path)
    if chain not in store:
        raise BadgeError(f"chain '{chain}' not found")
    entry = store.get(_badge_key(chain))
    if entry is None:
        return None
    return entry.get("value")


def clear_badge(store_path, chain: str) -> None:
    """Remove the badge from a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise BadgeError(f"chain '{chain}' not found")
    key = _badge_key(chain)
    if key not in store:
        raise BadgeError(f"chain '{chain}' has no badge set")
    del store[key]
    save_store(store_path, store)


def list_badges(store_path) -> dict[str, str]:
    """Return a mapping of chain name -> badge for all chains that have one."""
    store = load_store(store_path)
    prefix = "__badge__"
    result = {}
    for key, val in store.items():
        if key.startswith(prefix):
            chain = key[len(prefix):]
            result[chain] = val.get("value", "")
    return result
