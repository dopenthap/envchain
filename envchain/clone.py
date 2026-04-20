"""Clone a chain into a new chain, optionally under a different project namespace."""

from envchain.storage import load_store, save_store
from envchain.lock import assert_unlocked


class CloneError(Exception):
    pass


def clone_chain(src: str, dst: str, store_path, *, overwrite: bool = False) -> dict:
    """Clone chain *src* into *dst*.

    Returns the cloned variable dict.
    Raises CloneError if src is missing, dst already exists (unless overwrite=True),
    or src is locked.
    """
    store = load_store(store_path)

    if src not in store:
        raise CloneError(f"source chain '{src}' not found")

    assert_unlocked(src, store_path)

    if dst in store and not overwrite:
        raise CloneError(
            f"destination chain '{dst}' already exists; use --overwrite to replace it"
        )

    # Deep-copy the variable mapping so mutations to dst don't affect src
    store[dst] = dict(store[src])
    save_store(store_path, store)
    return store[dst]
