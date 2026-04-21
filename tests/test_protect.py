import pytest
from pathlib import Path
from envchain.storage import save_store
from envchain.protect import (
    protect_chain,
    unprotect_chain,
    is_protected,
    assert_unprotected,
    list_protected,
    ProtectError,
)


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


def write_store(path, data):
    save_store(path, data)


def test_protect_chain(store_path):
    write_store(store_path, {"prod": {"KEY": "val"}})
    protect_chain("prod", store_path)
    assert is_protected("prod", store_path) is True


def test_protect_missing_chain_raises(store_path):
    write_store(store_path, {})
    with pytest.raises(ProtectError, match="not found"):
        protect_chain("ghost", store_path)


def test_unprotect_chain(store_path):
    write_store(store_path, {"prod": {"KEY": "val"}})
    protect_chain("prod", store_path)
    unprotect_chain("prod", store_path)
    assert is_protected("prod", store_path) is False


def test_unprotect_not_protected_raises(store_path):
    write_store(store_path, {"prod": {"KEY": "val"}})
    with pytest.raises(ProtectError, match="is not protected"):
        unprotect_chain("prod", store_path)


def test_assert_unprotected_passes(store_path):
    write_store(store_path, {"dev": {"X": "1"}})
    # should not raise
    assert_unprotected("dev", store_path)


def test_assert_unprotected_raises(store_path):
    write_store(store_path, {"dev": {"X": "1"}})
    protect_chain("dev", store_path)
    with pytest.raises(ProtectError, match="unprotect it first"):
        assert_unprotected("dev", store_path)


def test_list_protected(store_path):
    write_store(store_path, {"a": {"K": "v"}, "b": {"K": "v"}, "c": {"K": "v"}})
    protect_chain("a", store_path)
    protect_chain("c", store_path)
    assert list_protected(store_path) == ["a", "c"]


def test_list_protected_empty(store_path):
    write_store(store_path, {"a": {"K": "v"}})
    assert list_protected(store_path) == []
