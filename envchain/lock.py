"""Lock/unlock chains to prevent accidental modification."""

from envchain.storage import load_store, save_store


class LockError(Exception):
    pass


def lock_chain(store_path, name: str) -> None:
    store = load_store(store_path)
    if name not in store.get("chains", {}):
        raise LockError(f"Chain '{name}' not found")
    store.setdefault("locks", {})[name] = True
    save_store(store_path, store)


def unlock_chain(store_path, name: str) -> None:
    store = load_store(store_path)
    locks = store.get("locks", {})
    if name not in locks:
        raise LockError(f"Chain '{name}' is not locked")
    del locks[name]
    if not locks:
        store.pop("locks", None)
    else:
        store["locks"] = locks
    save_store(store_path, store)


def is_locked(store_path, name: str) -> bool:
    store = load_store(store_path)
    return store.get("locks", {}).get(name, False)


def assert_unlocked(store_path, name: str) -> None:
    if is_locked(store_path, name):
        raise LockError(f"Chain '{name}' is locked. Use 'unlock' to modify it.")


def list_locked(store_path) -> list[str]:
    store = load_store(store_path)
    return sorted(k for k, v in store.get("locks", {}).items() if v)
