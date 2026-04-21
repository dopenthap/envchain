"""Chain inheritance — let one chain extend another, merging vars at load time."""

from envchain.storage import load_store, save_store


class InheritError(Exception):
    pass


def _inherit_key(chain: str) -> str:
    return f"__inherit__{chain}"


def set_parent(chain: str, parent: str, store_path) -> None:
    """Set `parent` as the base chain for `chain`."""
    store = load_store(store_path)
    if chain not in store:
        raise InheritError(f"chain '{chain}' not found")
    if parent not in store:
        raise InheritError(f"parent chain '{parent}' not found")
    if chain == parent:
        raise InheritError("a chain cannot inherit from itself")
    # Detect simple cycle: parent already inherits from chain
    meta = store.get(_inherit_key(parent))
    if isinstance(meta, dict) and meta.get("parent") == chain:
        raise InheritError(f"cycle detected: '{parent}' already inherits from '{chain}'")
    store[_inherit_key(chain)] = {"parent": parent}
    save_store(store_path, store)


def remove_parent(chain: str, store_path) -> None:
    """Remove inheritance from `chain`."""
    store = load_store(store_path)
    key = _inherit_key(chain)
    if key not in store:
        raise InheritError(f"chain '{chain}' has no parent set")
    del store[key]
    save_store(store_path, store)


def get_parent(chain: str, store_path) -> str | None:
    """Return the parent chain name, or None if not set."""
    store = load_store(store_path)
    meta = store.get(_inherit_key(chain))
    if meta is None:
        return None
    return meta.get("parent")


def resolve_chain(chain: str, store_path) -> dict:
    """Return merged env vars: parent vars first, child vars override."""
    store = load_store(store_path)
    if chain not in store:
        raise InheritError(f"chain '{chain}' not found")
    parent_name = get_parent(chain, store_path)
    merged = {}
    if parent_name:
        if parent_name not in store:
            raise InheritError(f"parent chain '{parent_name}' not found")
        merged.update(store[parent_name])
    merged.update(store[chain])
    return merged
