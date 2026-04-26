"""Checkpoint support for envchain.

A checkpoint is a named point-in-time snapshot of a chain that can be
quickly restored.  Unlike snapshots (which are auto-labelled and stored
inside the chain's own key-space), checkpoints are stored in a dedicated
section of the store so they are easy to enumerate across all chains.
"""

from __future__ import annotations

import datetime
from typing import Dict, List, Optional

from .storage import load_store, save_store, get_chain


class CheckpointError(Exception):
    """Raised when a checkpoint operation fails."""


def _cp_prefix(chain: str) -> str:
    return f"__checkpoint__{chain}__"


def _cp_key(chain: str, label: str) -> str:
    return f"{_cp_prefix(chain)}{label}"


def create_checkpoint(
    store_path,
    chain: str,
    label: Optional[str] = None,
) -> str:
    """Capture the current state of *chain* as a checkpoint.

    If *label* is omitted a timestamp-based label is generated.
    Returns the label used.

    Raises:
        CheckpointError: if *chain* does not exist.
    """
    store = load_store(store_path)
    if chain not in store:
        raise CheckpointError(f"chain '{chain}' not found")

    if label is None:
        label = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    key = _cp_key(chain, label)
    if key in store:
        raise CheckpointError(
            f"checkpoint '{label}' already exists for chain '{chain}'"
        )

    # Store a copy of the chain's vars under the checkpoint key
    store[key] = dict(store[chain])
    save_store(store_path, store)
    return label


def restore_checkpoint(store_path, chain: str, label: str) -> None:
    """Restore *chain* to the state saved in checkpoint *label*.

    Raises:
        CheckpointError: if the checkpoint does not exist.
    """
    store = load_store(store_path)
    key = _cp_key(chain, label)
    if key not in store:
        raise CheckpointError(
            f"checkpoint '{label}' not found for chain '{chain}'"
        )

    store[chain] = dict(store[key])
    save_store(store_path, store)


def delete_checkpoint(store_path, chain: str, label: str) -> None:
    """Remove a checkpoint.

    Raises:
        CheckpointError: if the checkpoint does not exist.
    """
    store = load_store(store_path)
    key = _cp_key(chain, label)
    if key not in store:
        raise CheckpointError(
            f"checkpoint '{label}' not found for chain '{chain}'"
        )

    del store[key]
    save_store(store_path, store)


def list_checkpoints(store_path, chain: str) -> List[str]:
    """Return all checkpoint labels for *chain*, sorted chronologically."""
    store = load_store(store_path)
    prefix = _cp_prefix(chain)
    labels = [
        k[len(prefix):]
        for k in store
        if k.startswith(prefix)
    ]
    return sorted(labels)


def get_checkpoint(store_path, chain: str, label: str) -> Dict[str, str]:
    """Return the vars stored in a checkpoint.

    Raises:
        CheckpointError: if the checkpoint does not exist.
    """
    store = load_store(store_path)
    key = _cp_key(chain, label)
    if key not in store:
        raise CheckpointError(
            f"checkpoint '{label}' not found for chain '{chain}'"
        )
    return dict(store[key])
