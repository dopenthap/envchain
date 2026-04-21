"""Group multiple chains under a named group for batch operations."""

from envchain.storage import load_store, save_store

GROUP_PREFIX = "__group__"


class GroupError(Exception):
    pass


def _group_key(group_name: str) -> str:
    return f"{GROUP_PREFIX}{group_name}"


def create_group(store_path, group_name: str, chains: list[str]) -> None:
    """Create or overwrite a group with the given chain names."""
    store = load_store(store_path)
    # Validate all chains exist
    for chain in chains:
        if chain not in store:
            raise GroupError(f"Chain not found: {chain}")
    key = _group_key(group_name)
    store[key] = {"members": chains}
    save_store(store_path, store)


def get_group(store_path, group_name: str) -> list[str]:
    """Return the list of chain names in a group."""
    store = load_store(store_path)
    key = _group_key(group_name)
    if key not in store:
        raise GroupError(f"Group not found: {group_name}")
    return store[key]["members"]


def delete_group(store_path, group_name: str) -> None:
    """Delete a group (does not delete the chains themselves)."""
    store = load_store(store_path)
    key = _group_key(group_name)
    if key not in store:
        raise GroupError(f"Group not found: {group_name}")
    del store[key]
    save_store(store_path, store)


def list_groups(store_path) -> dict[str, list[str]]:
    """Return all groups as {group_name: [chain, ...]}."""
    store = load_store(store_path)
    result = {}
    for key, value in store.items():
        if key.startswith(GROUP_PREFIX):
            group_name = key[len(GROUP_PREFIX):]
            result[group_name] = value.get("members", [])
    return result


def add_to_group(store_path, group_name: str, chain: str) -> None:
    """Add a chain to an existing group."""
    store = load_store(store_path)
    if chain not in store:
        raise GroupError(f"Chain not found: {chain}")
    key = _group_key(group_name)
    if key not in store:
        raise GroupError(f"Group not found: {group_name}")
    members = store[key]["members"]
    if chain not in members:
        members.append(chain)
        save_store(store_path, store)


def remove_from_group(store_path, group_name: str, chain: str) -> None:
    """Remove a chain from a group."""
    store = load_store(store_path)
    key = _group_key(group_name)
    if key not in store:
        raise GroupError(f"Group not found: {group_name}")
    members = store[key]["members"]
    if chain not in members:
        raise GroupError(f"Chain '{chain}' is not in group '{group_name}'")
    members.remove(chain)
    save_store(store_path, store)
