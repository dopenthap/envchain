"""Snapshot: save and restore chain states."""

from datetime import datetime
from envchain.storage import load_store, save_store


class SnapshotError(Exception):
    pass


def _snapshot_key(chain: str, label: str) -> str:
    return f"__snapshot__{chain}__{label}"


def create_snapshot(chain: str, label: str | None, store_path) -> str:
    store = load_store(store_path)
    if chain not in store:
        raise SnapshotError(f"Chain '{chain}' not found.")
    if label is None:
        label = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    key = _snapshot_key(chain, label)
    if key in store:
        raise SnapshotError(f"Snapshot '{label}' already exists for chain '{chain}'.")
    store[key] = dict(store[chain])
    save_store(store_path, store)
    return label


def restore_snapshot(chain: str, label: str, store_path, overwrite: bool = False) -> None:
    store = load_store(store_path)
    key = _snapshot_key(chain, label)
    if key not in store:
        raise SnapshotError(f"Snapshot '{label}' not found for chain '{chain}'.")
    if chain in store and not overwrite:
        raise SnapshotError(f"Chain '{chain}' already exists. Use overwrite=True to replace.")
    store[chain] = dict(store[key])
    save_store(store_path, store)


def list_snapshots(chain: str, store_path) -> list[str]:
    store = load_store(store_path)
    prefix = _snapshot_key(chain, "")
    return sorted(k[len(prefix):] for k in store if k.startswith(prefix))


def delete_snapshot(chain: str, label: str, store_path) -> None:
    store = load_store(store_path)
    key = _snapshot_key(chain, label)
    if key not in store:
        raise SnapshotError(f"Snapshot '{label}' not found for chain '{chain}'.")
    del store[key]
    save_store(store_path, store)
