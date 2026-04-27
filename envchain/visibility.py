"""Chain visibility: mark chains as public, private, or internal."""

from envchain.storage import load_store, save_store

VALID_LEVELS = ("public", "private", "internal")


class VisibilityError(Exception):
    pass


def _vis_key(chain: str) -> str:
    return f"__visibility__{chain}"


def set_visibility(store_path, chain: str, level: str) -> None:
    """Set the visibility level for a chain."""
    if level not in VALID_LEVELS:
        raise VisibilityError(
            f"Invalid visibility level {level!r}. Choose from: {', '.join(VALID_LEVELS)}"
        )
    store = load_store(store_path)
    if chain not in store:
        raise VisibilityError(f"Chain {chain!r} not found.")
    store[_vis_key(chain)] = level
    save_store(store_path, store)


def get_visibility(store_path, chain: str) -> str | None:
    """Return the visibility level for a chain, or None if not set."""
    store = load_store(store_path)
    if chain not in store:
        raise VisibilityError(f"Chain {chain!r} not found.")
    return store.get(_vis_key(chain))


def clear_visibility(store_path, chain: str) -> None:
    """Remove the visibility setting from a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise VisibilityError(f"Chain {chain!r} not found.")
    key = _vis_key(chain)
    if key not in store:
        raise VisibilityError(f"Chain {chain!r} has no visibility set.")
    del store[key]
    save_store(store_path, store)


def list_by_visibility(store_path, level: str) -> list[str]:
    """Return all chain names with the given visibility level."""
    if level not in VALID_LEVELS:
        raise VisibilityError(
            f"Invalid visibility level {level!r}. Choose from: {', '.join(VALID_LEVELS)}"
        )
    store = load_store(store_path)
    prefix = "__visibility__"
    return sorted(
        key[len(prefix):]
        for key, val in store.items()
        if key.startswith(prefix) and val == level
    )
