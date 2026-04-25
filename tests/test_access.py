"""Tests for envchain.access."""

import pytest

from envchain.storage import save_store
from envchain.access import (
    AccessError,
    set_access,
    remove_access,
    get_access,
    check_access,
    assert_access,
)


@pytest.fixture
def store_path(tmp_path):
    path = tmp_path / "store.json"
    save_store(path, {"prod": {"DB_URL": "postgres://localhost/prod"}})
    return path


def test_set_and_get_access(store_path):
    set_access(store_path, "prod", ["alice", "bob"])
    allowed = get_access(store_path, "prod")
    assert allowed == ["alice", "bob"]


def test_set_access_deduplicates(store_path):
    set_access(store_path, "prod", ["alice", "alice", "bob"])
    assert get_access(store_path, "prod") == ["alice", "bob"]


def test_get_access_not_set_returns_none(store_path):
    assert get_access(store_path, "prod") is None


def test_set_access_missing_chain_raises(store_path):
    with pytest.raises(AccessError, match="not found"):
        set_access(store_path, "ghost", ["alice"])


def test_set_access_empty_list_raises(store_path):
    with pytest.raises(AccessError, match="must not be empty"):
        set_access(store_path, "prod", [])


def test_remove_access(store_path):
    set_access(store_path, "prod", ["alice"])
    remove_access(store_path, "prod")
    assert get_access(store_path, "prod") is None


def test_remove_access_not_set_raises(store_path):
    with pytest.raises(AccessError, match="no access rules"):
        remove_access(store_path, "prod")


def test_check_access_no_restriction(store_path):
    assert check_access(store_path, "prod", user="anyone") is True


def test_check_access_allowed(store_path):
    set_access(store_path, "prod", ["alice"])
    assert check_access(store_path, "prod", user="alice") is True


def test_check_access_denied(store_path):
    set_access(store_path, "prod", ["alice"])
    assert check_access(store_path, "prod", user="mallory") is False


def test_assert_access_raises_for_denied(store_path):
    set_access(store_path, "prod", ["alice"])
    with pytest.raises(AccessError, match="not allowed"):
        assert_access(store_path, "prod", user="mallory")


def test_assert_access_passes_for_allowed(store_path):
    set_access(store_path, "prod", ["alice"])
    assert_access(store_path, "prod", user="alice")  # should not raise
