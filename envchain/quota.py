"""Per-chain key count quotas."""

from envchain.storage import load_store, save_store


class QuotaError(Exception):
    pass


def _quota_key(chain: str) -> str:
    return f"__quota__{chain}"


def set_quota(store_path, chain: str, limit: int) -> None:
    """Set a maximum number of keys allowed in a chain."""
    if limit < 1:
        raise QuotaError("Quota limit must be at least 1")
    store = load_store(store_path)
    if chain not in store:
        raise QuotaError(f"Chain '{chain}' not found")
    store[_quota_key(chain)] = limit
    save_store(store_path, store)


def remove_quota(store_path, chain: str) -> None:
    """Remove the quota for a chain."""
    store = load_store(store_path)
    key = _quota_key(chain)
    if key not in store:
        raise QuotaError(f"No quota set for chain '{chain}'")
    del store[key]
    save_store(store_path, store)


def get_quota(store_path, chain: str):
    """Return the quota limit for a chain, or None if not set."""
    store = load_store(store_path)
    if chain not in store:
        raise QuotaError(f"Chain '{chain}' not found")
    return store.get(_quota_key(chain))


def check_quota(store_path, chain: str) -> None:
    """Raise QuotaError if the chain has reached its key limit."""
    store = load_store(store_path)
    if chain not in store:
        raise QuotaError(f"Chain '{chain}' not found")
    limit = store.get(_quota_key(chain))
    if limit is None:
        return
    current_keys = [
        k for k in store.get(chain, {})
    ]
    if len(current_keys) >= limit:
        raise QuotaError(
            f"Chain '{chain}' has reached its quota of {limit} key(s)"
        )


def list_quotas(store_path) -> dict:
    """Return a dict of chain -> limit for all chains with quotas."""
    store = load_store(store_path)
    prefix = "__quota__"
    return {
        k[len(prefix):]: v
        for k, v in store.items()
        if k.startswith(prefix)
    }
