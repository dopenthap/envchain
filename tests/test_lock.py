import pytest
from pathlib import Path
from envchain.storage import save_store
from envchain.lock import lock_chain, unlock_chain, is_locked, assert_unlocked, list_locked, LockError


@pytest.fixture
def store_path(tmp_path):
    p = tmp_path / "store.json"
    save_store(p, {"chains": {"prod": {"KEY": "val"}, "dev": {"X": "1"}}})
    return p


def test_lock_chain(store_path):
    lock_chain(store_path, "prod")
    assert is_locked(store_path, "prod") is True


def test_unlock_chain(store_path):
    lock_chain(store_path, "prod")
    unlock_chain(store_path, "prod")
    assert is_locked(store_path, "prod") is False


def test_lock_missing_chain(store_path):
    with pytest.raises(LockError, match="not found"):
        lock_chain(store_path, "ghost")


def test_unlock_not_locked(store_path):
    with pytest.raises(LockError, match="not locked"):
        unlock_chain(store_path, "prod")


def test_assert_unlocked_passes(store_path):
    assert_unlocked(store_path, "prod")  # no error


def test_assert_unlocked_raises(store_path):
    lock_chain(store_path, "prod")
    with pytest.raises(LockError, match="locked"):
        assert_unlocked(store_path, "prod")


def test_list_locked(store_path):
    lock_chain(store_path, "prod")
    lock_chain(store_path, "dev")
    assert list_locked(store_path) == ["dev", "prod"]


def test_list_locked_empty(store_path):
    assert list_locked(store_path) == []


def test_unlock_cleans_up_locks_key(store_path):
    lock_chain(store_path, "prod")
    unlock_chain(store_path, "prod")
    from envchain.storage import load_store
    store = load_store(store_path)
    assert "locks" not in store
