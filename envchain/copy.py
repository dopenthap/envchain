"""Copy/duplicate chains between names or projects."""

from envchain.storage import load_store, save_store, get_store_path


def copy_chain(src_chain: str, dst_chain: str, store_path=None, overwrite: bool = False) -> dict:
    """Copy all vars from src_chain to dst_chain.

    Returns the vars that were copied.
    Raises KeyError if src_chain doesn't exist.
    Raises ValueError if dst_chain already exists and overwrite=False.
    """
    if store_path is None:
        store_path = get_store_path()

    store = load_store(store_path)

    if src_chain not in store:
        raise KeyError(f"Chain '{src_chain}' does not exist.")

    if dst_chain in store and not overwrite:
        raise ValueError(
            f"Chain '{dst_chain}' already exists. Use overwrite=True to replace it."
        )

    store[dst_chain] = dict(store[src_chain])
    save_store(store_path, store)

    return dict(store[dst_chain])


def rename_chain(src_chain: str, dst_chain: str, store_path=None, overwrite: bool = False) -> dict:
    """Rename src_chain to dst_chain (copy + delete src)."""
    if store_path is None:
        store_path = get_store_path()

    copied = copy_chain(src_chain, dst_chain, store_path=store_path, overwrite=overwrite)

    store = load_store(store_path)
    del store[src_chain]
    save_store(store_path, store)

    return copied
