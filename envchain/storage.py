"""Handles reading and writing envchain data to disk."""

import json
import os
from pathlib import Path
from typing import Dict, Optional

DEFAULT_STORE_PATH = Path.home() / ".envchain" / "chains.json"


def get_store_path() -> Path:
    """Return the store path, allowing override via env var."""
    custom = os.environ.get("ENVCHAIN_STORE")
    return Path(custom) if custom else DEFAULT_STORE_PATH


def load_store(store_path: Optional[Path] = None) -> Dict[str, Dict[str, str]]:
    """Load all chains from disk. Returns empty dict if file doesn't exist."""
    path = store_path or get_store_path()
    if not path.exists():
        return {}
    with open(path, "r") as f:
        return json.load(f)


def save_store(data: Dict[str, Dict[str, str]], store_path: Optional[Path] = None) -> None:
    """Persist all chains to disk."""
    path = store_path or get_store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def get_chain(name: str, store_path: Optional[Path] = None) -> Optional[Dict[str, str]]:
    """Fetch a single chain by name. Returns None if not found."""
    store = load_store(store_path)
    return store.get(name)


def set_chain(name: str, env_vars: Dict[str, str], store_path: Optional[Path] = None) -> None:
    """Create or overwrite a chain."""
    store = load_store(store_path)
    store[name] = env_vars
    save_store(store, store_path)


def delete_chain(name: str, store_path: Optional[Path] = None) -> bool:
    """Delete a chain. Returns True if it existed, False otherwise."""
    store = load_store(store_path)
    if name not in store:
        return False
    del store[name]
    save_store(store, store_path)
    return True


def list_chains(store_path: Optional[Path] = None) -> list:
    """Return sorted list of chain names."""
    store = load_store(store_path)
    return sorted(store.keys())
