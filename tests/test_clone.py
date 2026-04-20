import pytest
from pathlib import Path
from envchain.clone import clone_chain, CloneError
from envchain.storage import load_store, save_store
from envchain.lock import lock_chain


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


def _setup(store_path):
    data = {
        "prod": {"DB_URL": "postgres://prod", "SECRET": "abc"},
        "staging": {"DB_URL": "postgres://staging"},
    }
    save_store(store_path, data)
    return data


def test_clone_creates_dst(store_path):
    _setup(store_path)
    result = clone_chain("prod", "prod-backup", store_path)
    assert result == {"DB_URL": "postgres://prod", "SECRET": "abc"}
    store = load_store(store_path)
    assert "prod-backup" in store


def test_clone_does_not_mutate_src(store_path):
    _setup(store_path)
    clone_chain("prod", "prod-copy", store_path)
    store = load_store(store_path)
    # Mutate the clone and verify src is unchanged
    store["prod-copy"]["NEW_KEY"] = "val"
    save_store(store_path, store)
    store2 = load_store(store_path)
    assert "NEW_KEY" not in store2["prod"]


def test_clone_missing_src_raises(store_path):
    _setup(store_path)
    with pytest.raises(CloneError, match="source chain 'nope' not found"):
        clone_chain("nope", "dst", store_path)


def test_clone_dst_exists_no_overwrite(store_path):
    _setup(store_path)
    with pytest.raises(CloneError, match="already exists"):
        clone_chain("prod", "staging", store_path)


def test_clone_dst_exists_with_overwrite(store_path):
    _setup(store_path)
    result = clone_chain("prod", "staging", store_path, overwrite=True)
    assert result["SECRET"] == "abc"
    store = load_store(store_path)
    assert store["staging"] == {"DB_URL": "postgres://prod", "SECRET": "abc"}


def test_clone_locked_src_raises(store_path):
    _setup(store_path)
    lock_chain("prod", store_path)
    with pytest.raises(Exception, match="locked"):
        clone_chain("prod", "prod-clone", store_path)
