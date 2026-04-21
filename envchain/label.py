"""Label management for envchain chains."""

from envchain.storage import load_store, save_store


class LabelError(Exception):
    pass


def _label_key(chain: str) -> str:
    return f"__label__{chain}"


def set_label(store_path, chain: str, label: str) -> None:
    """Set a human-friendly display label for a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise LabelError(f"Chain '{chain}' not found.")
    if not label or not label.strip():
        raise LabelError("Label must not be empty.")
    store[_label_key(chain)] = {"value": label.strip()}
    save_store(store_path, store)


def get_label(store_path, chain: str) -> str | None:
    """Return the label for a chain, or None if not set."""
    store = load_store(store_path)
    if chain not in store:
        raise LabelError(f"Chain '{chain}' not found.")
    entry = store.get(_label_key(chain))
    return entry["value"] if entry else None


def clear_label(store_path, chain: str) -> None:
    """Remove the label from a chain."""
    store = load_store(store_path)
    if chain not in store:
        raise LabelError(f"Chain '{chain}' not found.")
    key = _label_key(chain)
    if key not in store:
        raise LabelError(f"Chain '{chain}' has no label set.")
    del store[key]
    save_store(store_path, store)


def list_labels(store_path) -> dict:
    """Return a mapping of chain name -> label for all labelled chains."""
    store = load_store(store_path)
    prefix = "__label__"
    result = {}
    for key, val in store.items():
        if key.startswith(prefix):
            chain = key[len(prefix):]
            if chain in store:
                result[chain] = val["value"]
    return result
