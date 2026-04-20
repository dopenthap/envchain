"""Rename a chain in the store, preserving all metadata keys."""

from envchain.storage import load_store, save_store


class RenameError(Exception):
    pass


META_PREFIXES = ("__tags__", "__locked__", "__snapshot:", "__pin:", "__alias:", "__schedule:")


def _meta_keys_for(chain: str, store: dict) -> list[str]:
    """Return all top-level store keys that belong to metadata for *chain*."""
    results = []
    for key in store:
        if key == f"__tags__{chain}":
            results.append(key)
        elif key == f"__locked__{chain}":
            results.append(key)
        elif key.startswith(f"__snapshot:{chain}:"):
            results.append(key)
        elif key.startswith(f"__pin:{chain}:"):
            results.append(key)
        elif key.startswith(f"__schedule:{chain}:"):
            results.append(key)
    return results


def rename_chain(store_path, src: str, dst: str, overwrite: bool = False) -> None:
    """Rename chain *src* to *dst* in the store at *store_path*.

    Raises RenameError if:
    - *src* does not exist
    - *dst* already exists and *overwrite* is False
    """
    store = load_store(store_path)

    if src not in store:
        raise RenameError(f"chain '{src}' not found")

    if dst in store and not overwrite:
        raise RenameError(
            f"chain '{dst}' already exists; use overwrite=True to replace it"
        )

    # Move the chain data
    store[dst] = store.pop(src)

    # Move associated metadata keys
    for meta_key in _meta_keys_for(src, list(store.keys())):
        new_key = meta_key.replace(f":{src}:", f":{dst}:", 1)
        # Handle simple suffix-based keys (tags, locked)
        if meta_key.endswith(src):
            new_key = meta_key[: -len(src)] + dst
        store[new_key] = store.pop(meta_key)

    save_store(store_path, store)
