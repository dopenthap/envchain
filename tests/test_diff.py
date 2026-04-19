import json
import pytest
from pathlib import Path
from envchain.storage import save_store
from envchain.diff import diff_chains
from envchain.merge import ChainNotFoundError


@pytest.fixture
def store_path(tmp_path):
    return str(tmp_path / "store.json")


def _setup(store_path):
    store = {
        "dev": {"DB_URL": "localhost", "DEBUG": "true", "SHARED": "same"},
        "prod": {"DB_URL": "prod.db.host", "API_KEY": "secret", "SHARED": "same"},
    }
    save_store(store_path, store)


def test_diff_only_in_a(store_path):
    _setup(store_path)
    result = diff_chains(store_path, "dev", "prod")
    assert result["only_in_a"] == {"DEBUG": "true"}


def test_diff_only_in_b(store_path):
    _setup(store_path)
    result = diff_chains(store_path, "dev", "prod")
    assert result["only_in_b"] == {"API_KEY": "secret"}


def test_diff_changed(store_path):
    _setup(store_path)
    result = diff_chains(store_path, "dev", "prod")
    assert result["changed"] == {"DB_URL": {"a": "localhost", "b": "prod.db.host"}}


def test_diff_same(store_path):
    _setup(store_path)
    result = diff_chains(store_path, "dev", "prod")
    assert result["same"] == {"SHARED": "same"}


def test_diff_identical_chains(store_path):
    store = {"a": {"X": "1"}, "b": {"X": "1"}}
    save_store(store_path, store)
    result = diff_chains(store_path, "a", "b")
    assert result["only_in_a"] == {}
    assert result["only_in_b"] == {}
    assert result["changed"] == {}
    assert result["same"] == {"X": "1"}


def test_diff_missing_chain_a(store_path):
    _setup(store_path)
    with pytest.raises(ChainNotFoundError, match="dev2"):
        diff_chains(store_path, "dev2", "prod")


def test_diff_missing_chain_b(store_path):
    _setup(store_path)
    with pytest.raises(ChainNotFoundError, match="staging"):
        diff_chains(store_path, "dev", "staging")
