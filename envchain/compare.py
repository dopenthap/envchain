"""Compare two chains and produce a structured summary of differences and similarities."""

from dataclasses import dataclass, field
from typing import Dict, List
from envchain.storage import load_store


class CompareError(Exception):
    pass


@dataclass
class CompareResult:
    chain_a: str
    chain_b: str
    only_in_a: List[str] = field(default_factory=list)
    only_in_b: List[str] = field(default_factory=list)
    shared_same: List[str] = field(default_factory=list)
    shared_different: List[str] = field(default_factory=list)

    def has_differences(self) -> bool:
        return bool(self.only_in_a or self.only_in_b or self.shared_different)

    def summary(self) -> Dict[str, int]:
        return {
            "only_in_a": len(self.only_in_a),
            "only_in_b": len(self.only_in_b),
            "shared_same": len(self.shared_same),
            "shared_different": len(self.shared_different),
        }


def compare_chains(store_path, chain_a: str, chain_b: str) -> CompareResult:
    store = load_store(store_path)
    chains = store.get("chains", {})

    if chain_a not in chains:
        raise CompareError(f"Chain not found: {chain_a}")
    if chain_b not in chains:
        raise CompareError(f"Chain not found: {chain_b}")

    vars_a: Dict[str, str] = chains[chain_a]
    vars_b: Dict[str, str] = chains[chain_b]

    keys_a = set(vars_a)
    keys_b = set(vars_b)

    result = CompareResult(chain_a=chain_a, chain_b=chain_b)
    result.only_in_a = sorted(keys_a - keys_b)
    result.only_in_b = sorted(keys_b - keys_a)

    for key in sorted(keys_a & keys_b):
        if vars_a[key] == vars_b[key]:
            result.shared_same.append(key)
        else:
            result.shared_different.append(key)

    return result
