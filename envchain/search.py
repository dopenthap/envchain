"""Search across chains for keys or values matching a pattern."""

from __future__ import annotations
import re
from typing import NamedTuple

from envchain.storage import load_store


class SearchResult(NamedTuple):
    chain: str
    key: str
    value: str


class SearchError(Exception):
    pass


def search_chains(
    store_path,
    pattern: str,
    *,
    search_keys: bool = True,
    search_values: bool = False,
    chain_filter: str | None = None,
    ignore_case: bool = False,
) -> list[SearchResult]:
    """Return all (chain, key, value) triples matching *pattern*.

    By default only key names are searched. Pass search_values=True to
    also (or exclusively) match against values.
    """
    flags = re.IGNORECASE if ignore_case else 0
    try:
        rx = re.compile(pattern, flags)
    except re.error as exc:
        raise SearchError(f"Invalid pattern: {exc}") from exc

    store = load_store(store_path)
    results: list[SearchResult] = []

    for chain_name, vars_ in store.get("chains", {}).items():
        if chain_filter and chain_name != chain_filter:
            continue
        for key, value in vars_.items():
            matched = (search_keys and rx.search(key)) or (
                search_values and rx.search(value)
            )
            if matched:
                results.append(SearchResult(chain=chain_name, key=key, value=value))

    results.sort(key=lambda r: (r.chain, r.key))
    return results
