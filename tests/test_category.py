"""Tests for envchain.category."""

import pytest

from envchain.storage import save_store
from envchain.category import (
    CategoryError,
    set_category,
    get_category,
    clear_category,
    list_by_category,
)


@pytest.fixture()
def store_path(tmp_path):
    path = tmp_path / "store.json"
    save_store(path, {
        "prod": {"API_KEY": "abc"},
        "staging": {"API_KEY": "def"},
        "dev": {"API_KEY": "ghi"},
    })
    return path


def test_set_and_get_category(store_path):
    set_category(store_path, "prod", "backend")
    assert get_category(store_path, "prod") == "backend"


def test_get_category_not_set_returns_none(store_path):
    assert get_category(store_path, "dev") is None


def test_set_category_strips_whitespace(store_path):
    set_category(store_path, "staging", "  infra  ")
    assert get_category(store_path, "staging") == "infra"


def test_set_category_empty_raises(store_path):
    with pytest.raises(CategoryError, match="must not be empty"):
        set_category(store_path, "prod", "   ")


def test_set_category_missing_chain_raises(store_path):
    with pytest.raises(CategoryError, match="not found"):
        set_category(store_path, "ghost", "backend")


def test_get_category_missing_chain_raises(store_path):
    with pytest.raises(CategoryError, match="not found"):
        get_category(store_path, "ghost")


def test_clear_category(store_path):
    set_category(store_path, "prod", "backend")
    clear_category(store_path, "prod")
    assert get_category(store_path, "prod") is None


def test_clear_category_not_set_raises(store_path):
    with pytest.raises(CategoryError, match="no category set"):
        clear_category(store_path, "dev")


def test_clear_category_missing_chain_raises(store_path):
    with pytest.raises(CategoryError, match="not found"):
        clear_category(store_path, "ghost")


def test_list_by_category(store_path):
    set_category(store_path, "prod", "backend")
    set_category(store_path, "staging", "backend")
    set_category(store_path, "dev", "local")
    result = list_by_category(store_path)
    assert result == {
        "backend": ["prod", "staging"],
        "local": ["dev"],
    }


def test_list_by_category_empty(store_path):
    assert list_by_category(store_path) == {}
