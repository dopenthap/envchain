"""Chain rating/scoring module for envchain."""

from __future__ import annotations

from envchain.storage import load_store, save_store


class RatingError(Exception):
    pass


VALID_RATINGS = {1, 2, 3, 4, 5}


def _rating_key(chain: str) -> str:
    return f"__meta__.{chain}.rating"


def set_rating(store_path, chain: str, rating: int) -> None:
    """Set an integer rating (1-5) for a chain."""
    if rating not in VALID_RATINGS:
        raise RatingError(f"Rating must be between 1 and 5, got {rating}")
    store = load_store(store_path)
    if chain not in store:
        raise RatingError(f"Chain '{chain}' not found")
    store[_rating_key(chain)] = str(rating)
    save_store(store_path, store)


def get_rating(store_path, chain: str) -> int | None:
    """Return the rating for a chain, or None if not set."""
    store = load_store(store_path)
    if chain not in store:
        raise RatingError(f"Chain '{chain}' not found")
    raw = store.get(_rating_key(chain))
    return int(raw) if raw is not None else None


def clear_rating(store_path, chain: str) -> None:
    """Remove the rating for a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise RatingError(f"Chain '{chain}' not found")
    key = _rating_key(chain)
    if key not in store:
        raise RatingError(f"Chain '{chain}' has no rating set")
    del store[key]
    save_store(store_path, store)


def list_ratings(store_path) -> dict[str, int]:
    """Return a dict of chain -> rating for all rated chains."""
    store = load_store(store_path)
    result = {}
    prefix = "__meta__."
    suffix = ".rating"
    for key, val in store.items():
        if key.startswith(prefix) and key.endswith(suffix):
            chain = key[len(prefix):-len(suffix)]
            if chain in store:
                result[chain] = int(val)
    return result
