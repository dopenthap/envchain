"""Tests for envchain.ttl"""

import time
import pytest

from envchain.storage import save_store
from envchain.ttl import (
    TtlError,
    get_ttl,
    is_expired,
    list_ttls,
    remove_ttl,
    set_ttl,
)


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {"mychain": {"KEY": "val"}, "other": {"X": "1"}})
    return store_path


def test_set_and_get_ttl(populated):
    set_ttl(populated, "mychain", 300)
    info = get_ttl(populated, "mychain")
    assert info is not None
    assert info["seconds"] == 300
    assert info["expires_at"] > time.time()


def test_get_ttl_not_set_returns_none(populated):
    assert get_ttl(populated, "mychain") is None


def test_set_ttl_missing_chain_raises(populated):
    with pytest.raises(TtlError, match="not found"):
        set_ttl(populated, "ghost", 60)


def test_set_ttl_zero_raises(populated):
    with pytest.raises(TtlError, match="positive"):
        set_ttl(populated, "mychain", 0)


def test_set_ttl_negative_raises(populated):
    with pytest.raises(TtlError, match="positive"):
        set_ttl(populated, "mychain", -10)


def test_remove_ttl(populated):
    set_ttl(populated, "mychain", 100)
    remove_ttl(populated, "mychain")
    assert get_ttl(populated, "mychain") is None


def test_remove_ttl_not_set_raises(populated):
    with pytest.raises(TtlError, match="no TTL set"):
        remove_ttl(populated, "mychain")


def test_is_expired_false_for_future(populated):
    set_ttl(populated, "mychain", 9999)
    assert is_expired(populated, "mychain") is False


def test_is_expired_true_for_past(populated):
    set_ttl(populated, "mychain", 1)
    # Manually backdate the expiry
    from envchain.storage import load_store, save_store as _save
    store = load_store(populated)
    store["__ttl__mychain"]["expires_at"] = time.time() - 10
    _save(populated, store)
    assert is_expired(populated, "mychain") is True


def test_is_expired_no_ttl_returns_false(populated):
    assert is_expired(populated, "mychain") is False


def test_list_ttls(populated):
    set_ttl(populated, "mychain", 60)
    set_ttl(populated, "other", 120)
    result = list_ttls(populated)
    assert set(result.keys()) == {"mychain", "other"}
    assert result["mychain"]["seconds"] == 60
    assert result["other"]["seconds"] == 120
