"""Tests for envchain.expire."""

from __future__ import annotations

import datetime
import json
import pytest

from envchain.expire import (
    ExpireError,
    get_expiry,
    is_expired,
    list_expiries,
    remove_expiry,
    set_expiry,
)


@pytest.fixture
def store_path(tmp_path):
    path = tmp_path / "store.json"
    data = {
        "mychain": {"KEY": "value"},
        "other": {"FOO": "bar"},
    }
    path.write_text(json.dumps(data))
    return path


def _future() -> datetime.datetime:
    return datetime.datetime.utcnow() + datetime.timedelta(days=7)


def _past() -> datetime.datetime:
    return datetime.datetime.utcnow() - datetime.timedelta(days=1)


def test_set_and_get_expiry(store_path):
    exp = _future()
    set_expiry(store_path, "mychain", exp)
    result = get_expiry(store_path, "mychain")
    assert result is not None
    assert abs((result - exp).total_seconds()) < 1


def test_get_expiry_not_set_returns_none(store_path):
    assert get_expiry(store_path, "mychain") is None


def test_set_expiry_missing_chain_raises(store_path):
    with pytest.raises(ExpireError, match="not found"):
        set_expiry(store_path, "ghost", _future())


def test_get_expiry_missing_chain_raises(store_path):
    with pytest.raises(ExpireError, match="not found"):
        get_expiry(store_path, "ghost")


def test_remove_expiry(store_path):
    set_expiry(store_path, "mychain", _future())
    remove_expiry(store_path, "mychain")
    assert get_expiry(store_path, "mychain") is None


def test_remove_expiry_not_set_raises(store_path):
    with pytest.raises(ExpireError, match="no expiry"):
        remove_expiry(store_path, "mychain")


def test_is_expired_future(store_path):
    set_expiry(store_path, "mychain", _future())
    assert is_expired(store_path, "mychain") is False


def test_is_expired_past(store_path):
    set_expiry(store_path, "mychain", _past())
    assert is_expired(store_path, "mychain") is True


def test_is_expired_no_expiry(store_path):
    assert is_expired(store_path, "mychain") is False


def test_list_expiries(store_path):
    exp1 = _future()
    exp2 = _past()
    set_expiry(store_path, "mychain", exp1)
    set_expiry(store_path, "other", exp2)
    result = list_expiries(store_path)
    assert set(result.keys()) == {"mychain", "other"}
    assert abs((result["mychain"] - exp1).total_seconds()) < 1
    assert abs((result["other"] - exp2).total_seconds()) < 1


def test_list_expiries_empty(store_path):
    assert list_expiries(store_path) == {}
