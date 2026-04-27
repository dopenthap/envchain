"""Tests for envchain.region."""

import pytest

from envchain.region import (
    RegionError,
    clear_region,
    get_region,
    list_by_region,
    set_region,
)
from envchain.storage import save_store


@pytest.fixture()
def store_path(tmp_path):
    path = tmp_path / "store.json"
    save_store(path, {"mychain": {"KEY": "val"}, "other": {"X": "1"}})
    return path


def test_set_and_get_region(store_path):
    set_region(store_path, "mychain", "prod")
    assert get_region(store_path, "mychain") == "prod"


def test_get_region_not_set_returns_none(store_path):
    assert get_region(store_path, "mychain") is None


def test_set_region_invalid_raises(store_path):
    with pytest.raises(RegionError, match="Invalid region"):
        set_region(store_path, "mychain", "galaxy")


def test_set_region_missing_chain_raises(store_path):
    with pytest.raises(RegionError, match="not found"):
        set_region(store_path, "ghost", "dev")


def test_get_region_missing_chain_raises(store_path):
    with pytest.raises(RegionError, match="not found"):
        get_region(store_path, "ghost")


def test_clear_region(store_path):
    set_region(store_path, "mychain", "staging")
    clear_region(store_path, "mychain")
    assert get_region(store_path, "mychain") is None


def test_clear_region_not_set_raises(store_path):
    with pytest.raises(RegionError, match="no region set"):
        clear_region(store_path, "mychain")


def test_clear_region_missing_chain_raises(store_path):
    with pytest.raises(RegionError, match="not found"):
        clear_region(store_path, "ghost")


def test_list_by_region(store_path):
    set_region(store_path, "mychain", "prod")
    set_region(store_path, "other", "prod")
    result = list_by_region(store_path, "prod")
    assert result == ["mychain", "other"]


def test_list_by_region_empty(store_path):
    assert list_by_region(store_path, "dev") == []


def test_list_by_region_invalid_raises(store_path):
    with pytest.raises(RegionError, match="Invalid region"):
        list_by_region(store_path, "narnia")
