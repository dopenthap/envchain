"""Chain status summary — aggregates metadata for a chain into a single view."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from envchain.storage import load_store
from envchain.lock import is_locked
from envchain.protect import is_protected
from envchain.freeze import is_frozen
from envchain.describe import get_description
from envchain.tag import get_tags
from envchain.expire import get_expiry, is_expired


class StatusError(Exception):
    pass


@dataclass
class ChainStatus:
    name: str
    key_count: int
    locked: bool
    protected: bool
    frozen: bool
    description: Optional[str]
    tags: list[str] = field(default_factory=list)
    expiry: Optional[str] = None
    expired: bool = False

    def summary(self) -> str:
        flags = []
        if self.locked:
            flags.append("locked")
        if self.protected:
            flags.append("protected")
        if self.frozen:
            flags.append("frozen")
        if self.expired:
            flags.append("EXPIRED")
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        desc_str = f"\n  description : {self.description}" if self.description else ""
        tags_str = f"\n  tags        : {', '.join(self.tags)}" if self.tags else ""
        expiry_str = f"\n  expires     : {self.expiry}" if self.expiry else ""
        return (
            f"chain       : {self.name}{flag_str}\n"
            f"  keys      : {self.key_count}"
            f"{desc_str}{tags_str}{expiry_str}"
        )


def get_status(chain: str, store_path=None) -> ChainStatus:
    store = load_store(store_path)
    if chain not in store:
        raise StatusError(f"chain '{chain}' not found")

    keys = [
        k for k in store[chain]
        if not k.startswith("__")
    ]

    expiry = get_expiry(chain, store_path)
    expired = is_expired(chain, store_path) if expiry else False

    return ChainStatus(
        name=chain,
        key_count=len(keys),
        locked=is_locked(chain, store_path),
        protected=is_protected(chain, store_path),
        frozen=is_frozen(chain, store_path),
        description=get_description(chain, store_path),
        tags=get_tags(chain, store_path),
        expiry=expiry,
        expired=expired,
    )
