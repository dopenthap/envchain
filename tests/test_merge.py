import pytest
from pathlib import Path
from unittest.mock import patch

from envchain.merge import merge_chains, ChainNotFoundError
from envchain.storage import load_store, save_store, get_store_path


@pytest.fixture
def store_path(tmp_path):
    path = tmp_path / "test_project" / "store.json"
    with patch("envchain.merge.get_store_path", return_value=path):
        yield path


def _setup_store(store_path, data):
    store_path.parent.mkdir(parents=True, exist_ok=True)
    save_store(store_path, data)


def test_merge_no_overwrite(store_path):
    _setup_store(store_path, {
        "base": {"A": "1", "B": "2"},
        "extra": {"B": "99", "C": "3"},
    })
    merged = merge_chains("extra", "base", "test_project", overwrite=False)
    assert merged["A"] == "1"
    assert merged["B"] == "2"  # dst wins
    assert merged["C"] == "3"


def test_merge_with_overwrite(store_path):
    _setup_store(store_path, {
        "base": {"A": "1", "B": "2"},
        "extra": {"B": "99", "C": "3"},
    })
    merged = merge_chains("extra", "base", "test_project", overwrite=True)
    assert merged["A"] == "1"
    assert merged["B"] == "99"  # src wins
    assert merged["C"] == "3"


def test_merge_persists(store_path):
    _setup_store(store_path, {
        "a": {"X": "10"},
        "b": {"Y": "20"},
    })
    merge_chains("a", "b", "test_project", overwrite=False)
    store = load_store(store_path)
    assert store["b"]["X"] == "10"
    assert store["b"]["Y"] == "20"


def test_merge_missing_src(store_path):
    _setup_store(store_path, {"b": {"Y": "20"}})
    with pytest.raises(ChainNotFoundError, match="Source chain"):
        merge_chains("a", "b", "test_project")


def test_merge_missing_dst(store_path):
    _setup_store(store_path, {"a": {"X": "10"}})
    with pytest.raises(ChainNotFoundError, match="Destination chain"):
        merge_chains("a", "b", "test_project")


def test_merge_does_not_mutate_src(store_path):
    _setup_store(store_path, {
        "src": {"K": "v"},
        "dst": {"M": "n"},
    })
    merge_chains("src", "dst", "test_project", overwrite=True)
    store = load_store(store_path)
    assert store["src"] == {"K": "v"}
