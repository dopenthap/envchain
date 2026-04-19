"""Merge two chains together, optionally overwriting existing keys."""

from envchain.storage import load_store, save_store, get_store_path


class ChainNotFoundError(Exception):
    pass


def merge_chains(src: str, dst: str, project: str, overwrite: bool = False) -> dict:
    """Merge src chain into dst chain within a project.

    Args:
        src: Source chain name.
        dst: Destination chain name.
        project: Project name (store key).
        overwrite: If True, src keys overwrite dst keys on conflict.

    Returns:
        The merged vars dict.

    Raises:
        ChainNotFoundError: If src or dst chain does not exist.
    """
    store_path = get_store_path(project)
    store = load_store(store_path)

    if src not in store:
        raise ChainNotFoundError(f"Source chain '{src}' not found.")
    if dst not in store:
        raise ChainNotFoundError(f"Destination chain '{dst}' not found.")

    src_vars = store[src].copy()
    dst_vars = store[dst].copy()

    if overwrite:
        merged = {**dst_vars, **src_vars}
    else:
        merged = {**src_vars, **dst_vars}

    store[dst] = merged
    save_store(store_path, store)
    return merged
