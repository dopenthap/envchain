"""Tests for envchain storage module."""

import json
import pytest
from pathlib import Path

from envchain.storage import (
    load_store,
    save_store,
    get_chain,
    set_chain,
    delete_chain,
    list_chains,
)


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "chains.json"


def test_load_store_missing_file(store_path):
    assert load_store(store_path) == {}


def test_save_and_load_store(store_path):
    data = {"prod": {"DB_URL": "postgres://prod"}}
    save_store(data, store_path)
    assert load_store(store_path) == data


def test_save_creates_parent_dirs(tmp_path):
    nested = tmp_path / "a" / "b" / "chains.json"
    save_store({"x": {"FOO": "bar"}}, nested)
    assert nested.exists()


def test_set_and_get_chain(store_path):
    set_chain("dev", {"DEBUG": "true", "PORT": "8080"}, store_path)
    chain = get_chain("dev", store_path)
    assert chain == {"DEBUG": "true", "PORT": "8080"}


def test_get_chain_missing(store_path):
    assert get_chain("nope", store_path) is None


def test_set_chain_overwrites(store_path):
    set_chain("dev", {"A": "1"}, store_path)
    set_chain("dev", {"A": "2", "B": "3"}, store_path)
    assert get_chain("dev", store_path) == {"A": "2", "B": "3"}


def test_delete_chain_existing(store_path):
    set_chain("staging", {"ENV": "staging"}, store_path)
    result = delete_chain("staging", store_path)
    assert result is True
    assert get_chain("staging", store_path) is None


def test_delete_chain_missing(store_path):
    assert delete_chain("ghost", store_path) is False


def test_list_chains(store_path):
    set_chain("prod", {}, store_path)
    set_chain("dev", {}, store_path)
    set_chain("staging", {}, store_path)
    assert list_chains(store_path) == ["dev", "prod", "staging"]


def test_list_chains_empty(store_path):
    assert list_chains(store_path) == []
