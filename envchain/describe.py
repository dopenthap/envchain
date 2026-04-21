"""Chain description/annotation support."""

from envchain.storage import load_store, save_store


class DescribeError(Exception):
    pass


def _desc_key(chain: str) -> str:
    return f"__meta__.{chain}.description"


def set_description(store_path, chain: str, text: str) -> None:
    """Set a human-readable description for a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise DescribeError(f"chain '{chain}' not found")
    store[_desc_key(chain)] = text
    save_store(store_path, store)


def get_description(store_path, chain: str) -> str | None:
    """Return the description for a chain, or None if not set."""
    store = load_store(store_path)
    if chain not in store:
        raise DescribeError(f"chain '{chain}' not found")
    return store.get(_desc_key(chain))


def clear_description(store_path, chain: str) -> None:
    """Remove the description for a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise DescribeError(f"chain '{chain}' not found")
    key = _desc_key(chain)
    if key in store:
        del store[key]
        save_store(store_path, store)


def list_descriptions(store_path) -> dict[str, str]:
    """Return a mapping of chain -> description for all chains that have one."""
    store = load_store(store_path)
    result = {}
    prefix = "__meta__."
    suffix = ".description"
    for k, v in store.items():
        if k.startswith(prefix) and k.endswith(suffix):
            chain = k[len(prefix):-len(suffix)]
            result[chain] = v
    return result
