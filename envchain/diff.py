from typing import Dict, Any
from envchain.storage import load_store, ChainNotFoundError


def diff_chains(store_path: str, chain_a: str, chain_b: str) -> Dict[str, Any]:
    """Compare two chains and return their differences.

    Returns a dict with:
      - only_in_a: keys only in chain_a
      - only_in_b: keys only in chain_b
      - changed: keys in both but with different values
      - same: keys with identical values
    """
    store = load_store(store_path)

    if chain_a not in store:
        raise ChainNotFoundError(f"Chain '{chain_a}' not found")
    if chain_b not in store:
        raise ChainNotFoundError(f"Chain '{chain_b}' not found")

    vars_a = store[chain_a]
    vars_b = store[chain_b]

    keys_a = set(vars_a.keys())
    keys_b = set(vars_b.keys())

    only_in_a = {k: vars_a[k] for k in keys_a - keys_b}
    only_in_b = {k: vars_b[k] for k in keys_b - keys_a}

    changed = {}
    same = {}
    for k in keys_a & keys_b:
        if vars_a[k] != vars_b[k]:
            changed[k] = {"a": vars_a[k], "b": vars_b[k]}
        else:
            same[k] = vars_a[k]

    return {
        "only_in_a": only_in_a,
        "only_in_b": only_in_b,
        "changed": changed,
        "same": same,
    }
