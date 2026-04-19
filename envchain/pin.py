"""Pin a chain to a specific version (snapshot label) for reproducibility."""

from envchain.storage import load_store, save_store
from envchain.snapshot import list_snapshots

PIN_KEY = "__pins__"


class PinError(Exception):
    pass


def pin_chain(store_path, chain, label):
    """Pin chain to a snapshot label."""
    store = load_store(store_path)
    if chain not in store:
        raise PinError(f"chain '{chain}' not found")
    snapshots = list_snapshots(store_path, chain)
    if label not in snapshots:
        raise PinError(f"snapshot '{label}' not found for chain '{chain}'")
    pins = store.setdefault(PIN_KEY, {})
    pins[chain] = label
    save_store(store_path, store)


def unpin_chain(store_path, chain):
    """Remove pin from chain."""
    store = load_store(store_path)
    pins = store.get(PIN_KEY, {})
    if chain not in pins:
        raise PinError(f"chain '{chain}' is not pinned")
    del pins[chain]
    save_store(store_path, store)


def get_pin(store_path, chain):
    """Return the pinned snapshot label for chain, or None."""
    store = load_store(store_path)
    return store.get(PIN_KEY, {}).get(chain)


def list_pins(store_path):
    """Return dict of chain -> pinned label."""
    store = load_store(store_path)
    return dict(store.get(PIN_KEY, {}))
