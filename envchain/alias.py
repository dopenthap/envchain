"""Chain alias support — assign short names to chains."""

from envchain.storage import load_store, save_store


class AliasError(Exception):
    pass


def _aliases(store: dict) -> dict:
    return store.setdefault("__aliases__", {})


def set_alias(store_path, alias: str, chain: str) -> None:
    store = load_store(store_path)
    if chain not in store.get("chains", {}):
        raise AliasError(f"chain '{chain}' does not exist")
    if alias.startswith("__"):
        raise AliasError(f"alias '{alias}' is reserved")
    _aliases(store)[alias] = chain
    save_store(store_path, store)


def remove_alias(store_path, alias: str) -> None:
    store = load_store(store_path)
    aliases = _aliases(store)
    if alias not in aliases:
        raise AliasError(f"alias '{alias}' not found")
    del aliases[alias]
    save_store(store_path, store)


def resolve_alias(store_path, name: str) -> str:
    """Return the chain name for an alias, or name itself if not an alias."""
    store = load_store(store_path)
    return _aliases(store).get(name, name)


def list_aliases(store_path) -> dict:
    store = load_store(store_path)
    return dict(_aliases(store))
