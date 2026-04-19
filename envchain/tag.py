"""Tag chains with labels for easier organization and filtering."""

from envchain.storage import load_store, save_store

TAGS_KEY = "__tags__"


class TagError(Exception):
    pass


def add_tag(store_path, chain: str, tag: str) -> None:
    store = load_store(store_path)
    if chain not in store:
        raise TagError(f"Chain '{chain}' not found")
    tags = store.setdefault(TAGS_KEY, {})
    chain_tags = set(tags.get(chain, []))
    chain_tags.add(tag)
    tags[chain] = sorted(chain_tags)
    save_store(store_path, store)


def remove_tag(store_path, chain: str, tag: str) -> None:
    store = load_store(store_path)
    tags = store.get(TAGS_KEY, {})
    chain_tags = set(tags.get(chain, []))
    if tag not in chain_tags:
        raise TagError(f"Tag '{tag}' not found on chain '{chain}'")
    chain_tags.discard(tag)
    tags[chain] = sorted(chain_tags)
    store[TAGS_KEY] = tags
    save_store(store_path, store)


def get_tags(store_path, chain: str) -> list[str]:
    store = load_store(store_path)
    return store.get(TAGS_KEY, {}).get(chain, [])


def find_by_tag(store_path, tag: str) -> list[str]:
    store = load_store(store_path)
    tags = store.get(TAGS_KEY, {})
    return sorted(chain for chain, chain_tags in tags.items() if tag in chain_tags)
