"""Lint chains for common issues like empty values, duplicate keys across chains, etc."""

from envchain.storage import load_store


class LintWarning:
    def __init__(self, chain: str, key: str, message: str):
        self.chain = chain
        self.key = key
        self.message = message

    def __repr__(self):
        return f"LintWarning({self.chain!r}, {self.key!r}, {self.message!r})"

    def __eq__(self, other):
        return (
            isinstance(other, LintWarning)
            and self.chain == other.chain
            and self.key == other.key
            and self.message == other.message
        )


def lint_store(store_path) -> list[LintWarning]:
    store = load_store(store_path)
    chains = {k: v for k, v in store.items() if not k.startswith("__")}
    warnings = []

    for chain, env in chains.items():
        if not isinstance(env, dict):
            continue
        for key, value in env.items():
            if value == "" or value is None:
                warnings.append(LintWarning(chain, key, "empty value"))
            if key != key.upper():
                warnings.append(LintWarning(chain, key, "key is not uppercase"))
            if " " in key:
                warnings.append(LintWarning(chain, key, "key contains spaces"))

    # detect duplicate values across chains (possible secret reuse)
    value_map: dict[str, list[tuple[str, str]]] = {}
    for chain, env in chains.items():
        if not isinstance(env, dict):
            continue
        for key, value in env.items():
            if value:
                value_map.setdefault(value, []).append((chain, key))

    for value, occurrences in value_map.items():
        if len(occurrences) > 1:
            for chain, key in occurrences:
                warnings.append(LintWarning(chain, key, "duplicate value shared across chains"))

    return warnings
