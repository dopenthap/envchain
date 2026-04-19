"""Validation helpers for chain names and variable keys."""

import re
from dataclasses import dataclass
from typing import List


CHAIN_NAME_RE = re.compile(r'^[a-zA-Z0-9_][a-zA-Z0-9_\-\.]*$')
KEY_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')


@dataclass
class ValidationError:
    field: str
    message: str

    def __repr__(self):
        return f"ValidationError({self.field!r}: {self.message})"

    def __eq__(self, other):
        return isinstance(other, ValidationError) and self.field == other.field and self.message == other.message


def validate_chain_name(name: str) -> List[ValidationError]:
    errors = []
    if not name:
        errors.append(ValidationError("chain", "chain name must not be empty"))
        return errors
    if not CHAIN_NAME_RE.match(name):
        errors.append(ValidationError("chain", f"invalid chain name {name!r}: use letters, digits, underscores, hyphens, dots"))
    if len(name) > 128:
        errors.append(ValidationError("chain", "chain name must be 128 characters or fewer"))
    return errors


def validate_key(key: str) -> List[ValidationError]:
    errors = []
    if not key:
        errors.append(ValidationError("key", "key must not be empty"))
        return errors
    if not KEY_RE.match(key):
        errors.append(ValidationError("key", f"invalid key {key!r}: use letters, digits, underscores, must not start with digit"))
    if len(key) > 256:
        errors.append(ValidationError("key", "key must be 256 characters or fewer"))
    return errors


def validate_chain_and_key(chain: str, key: str) -> List[ValidationError]:
    return validate_chain_name(chain) + validate_key(key)
