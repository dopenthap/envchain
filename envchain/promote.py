"""Promote variables from one chain into another, optionally with a prefix."""

from envchain.storage import load_store, save_store


class PromoteError(Exception):
    pass


def promote_chain(
    store_path,
    src: str,
    dst: str,
    keys: list[str] | None = None,
    prefix: str = "",
    overwrite: bool = False,
) -> dict[str, str]:
    """Copy selected (or all) keys from *src* into *dst*, optionally renaming
    them with *prefix*.  Returns a dict of the keys that were actually written.

    Raises PromoteError if:
    - src chain does not exist
    - dst chain does not exist
    - a key already exists in dst and overwrite=False
    """
    store = load_store(store_path)

    if src not in store:
        raise PromoteError(f"source chain '{src}' not found")
    if dst not in store:
        raise PromoteError(f"destination chain '{dst}' not found")

    src_vars: dict[str, str] = {
        k: v for k, v in store[src].items() if not k.startswith("__")
    }

    if keys is not None:
        missing = [k for k in keys if k not in src_vars]
        if missing:
            raise PromoteError(
                f"key(s) not found in '{src}': {', '.join(missing)}"
            )
        src_vars = {k: src_vars[k] for k in keys}

    dst_vars: dict[str, str] = {
        k: v for k, v in store[dst].items() if not k.startswith("__")
    }

    promoted: dict[str, str] = {}
    for k, v in src_vars.items():
        new_key = f"{prefix}{k}" if prefix else k
        if new_key in dst_vars and not overwrite:
            raise PromoteError(
                f"key '{new_key}' already exists in '{dst}'; use overwrite=True to replace"
            )
        promoted[new_key] = v

    store[dst].update(promoted)
    save_store(store_path, store)
    return promoted
