"""Category support for grouping chains by functional area."""

from __future__ import annotations

from envchain.storage import load_store, save_store

CATEGORY_KEY_PREFIX = "__category__"


class CategoryError(Exception):
    pass


def _category_key(chain: str) -> str:
    return f"{CATEGORY_KEY_PREFIX}{chain}"


def set_category(store_path, chain: str, category: str) -> None:
    """Assign a category label to a chain."""
    category = category.strip()
    if not category:
        raise CategoryError("Category must not be empty.")
    store = load_store(store_path)
    if chain not in store:
        raise CategoryError(f"Chain '{chain}' not found.")
    store[_category_key(chain)] = {"value": category}
    save_store(store_path, store)


def get_category(store_path, chain: str) -> str | None:
    """Return the category for a chain, or None if not set."""
    store = load_store(store_path)
    if chain not in store:
        raise CategoryError(f"Chain '{chain}' not found.")
    entry = store.get(_category_key(chain))
    if entry is None:
        return None
    return entry.get("value")


def clear_category(store_path, chain: str) -> None:
    """Remove the category assignment from a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise CategoryError(f"Chain '{chain}' not found.")
    key = _category_key(chain)
    if key not in store:
        raise CategoryError(f"Chain '{chain}' has no category set.")
    del store[key]
    save_store(store_path, store)


def list_by_category(store_path) -> dict[str, list[str]]:
    """Return a mapping of category -> [chain names], sorted."""
    store = load_store(store_path)
    result: dict[str, list[str]] = {}
    for key, entry in store.items():
        if key.startswith(CATEGORY_KEY_PREFIX):
            chain = key[len(CATEGORY_KEY_PREFIX):]
            category = entry.get("value", "")
            result.setdefault(category, []).append(chain)
    for chains in result.values():
        chains.sort()
    return dict(sorted(result.items()))
