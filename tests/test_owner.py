"""Tests for envchain.owner."""

import pytest

from envchain.owner import OwnerError, set_owner, get_owner, clear_owner, list_owners
from envchain.storage import save_store


@pytest.fixture()
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture()
def populated(store_path):
    save_store(store_path, {
        "prod": {"DB_URL": "postgres://prod"},
        "staging": {"DB_URL": "postgres://staging"},
    })
    return store_path


def test_set_and_get_owner(populated):
    set_owner("prod", "alice", store_path=populated)
    assert get_owner("prod", store_path=populated) == "alice"


def test_get_owner_not_set_returns_none(populated):
    assert get_owner("prod", store_path=populated) is None


def test_set_owner_strips_whitespace(populated):
    set_owner("prod", "  bob  ", store_path=populated)
    assert get_owner("prod", store_path=populated) == "bob"


def test_set_owner_missing_chain_raises(populated):
    with pytest.raises(OwnerError, match="not found"):
        set_owner("ghost", "carol", store_path=populated)


def test_get_owner_missing_chain_raises(populated):
    with pytest.raises(OwnerError, match="not found"):
        get_owner("ghost", store_path=populated)


def test_set_owner_empty_string_raises(populated):
    with pytest.raises(OwnerError, match="must not be empty"):
        set_owner("prod", "   ", store_path=populated)


def test_clear_owner(populated):
    set_owner("prod", "alice", store_path=populated)
    clear_owner("prod", store_path=populated)
    assert get_owner("prod", store_path=populated) is None


def test_clear_owner_missing_chain_raises(populated):
    with pytest.raises(OwnerError, match="not found"):
        clear_owner("ghost", store_path=populated)


def test_list_owners(populated):
    set_owner("prod", "alice", store_path=populated)
    set_owner("staging", "bob", store_path=populated)
    owners = list_owners(store_path=populated)
    assert owners == {"prod": "alice", "staging": "bob"}


def test_list_owners_empty(populated):
    assert list_owners(store_path=populated) == {}


def test_owner_overwrite(populated):
    set_owner("prod", "alice", store_path=populated)
    set_owner("prod", "dave", store_path=populated)
    assert get_owner("prod", store_path=populated) == "dave"
