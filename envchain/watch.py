"""Watch a chain for changes and run a command when it updates."""

import hashlib
import json
import subprocess
import time
from pathlib import Path

from envchain.storage import load_store, get_store_path
from envchain.shell import build_env


class WatchError(Exception):
    pass


def _chain_hash(chain_name: str, store_path: Path) -> str:
    store = load_store(store_path)
    chain = store.get("chains", {}).get(chain_name)
    if chain is None:
        raise WatchError(f"Chain '{chain_name}' not found.")
    serialized = json.dumps(chain, sort_keys=True).encode()
    return hashlib.sha256(serialized).hexdigest()


def watch_chain(
    chain_name: str,
    command: list[str],
    interval: float = 2.0,
    store_path: Path | None = None,
    max_iterations: int | None = None,
) -> None:
    if store_path is None:
        store_path = get_store_path()

    last_hash = None
    iterations = 0

    while True:
        try:
            current_hash = _chain_hash(chain_name, store_path)
        except WatchError as e:
            raise WatchError(str(e)) from e

        if current_hash != last_hash:
            if last_hash is not None:
                store = load_store(store_path)
                env = build_env(chain_name, store)
                subprocess.run(command, env=env)
            last_hash = current_hash

        iterations += 1
        if max_iterations is not None and iterations >= max_iterations:
            break

        time.sleep(interval)
