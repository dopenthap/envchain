import pytest
from pathlib import Path
from envchain.rename import rename_chain, RenameError
from envchain.storage import load_store, save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


def write_store(path, data):
    save_store(path, data)


def test_rename_basic(store_path):
    write_store(store_path, {"prod": {"KEY": "val"}})
    rename_chain(store_path, "prod", "production")
    store = load_store(store_path)
    assert "production" in store
    assert store["production"] == {"KEY": "val"}
    assert "prod" not in store


def test_rename_missing_src_raises(store_path):
    write_store(store_path, {})
    with pytest.raises(RenameError, match="not found"):
        rename_chain(store_path, "ghost", "newname")


def test_rename_dst_exists_no_overwrite(store_path):
    write_store(store_path, {"a": {"X": "1"}, "b": {"Y": "2"}})
    with pytest.raises(RenameError, match="already exists"):
        rename_chain(store_path, "a", "b")


def test_rename_dst_exists_with_overwrite(store_path):
    write_store(store_path, {"a": {"X": "1"}, "b": {"Y": "2"}})
    rename_chain(store_path, "a", "b", overwrite=True)
    store = load_store(store_path)
    assert store["b"] == {"X": "1"}
    assert "a" not in store


def test_rename_preserves_tags_metadata(store_path):
    write_store(
        store_path,
        {
            "dev": {"API_KEY": "abc"},
            "__tags__dev": ["infra", "backend"],
        },
    )
    rename_chain(store_path, "dev", "development")
    store = load_store(store_path)
    assert "__tags__development" in store
    assert store["__tags__development"] == ["infra", "backend"]
    assert "__tags__dev" not in store


def test_rename_preserves_locked_metadata(store_path):
    write_store(
        store_path,
        {
            "staging": {"DB": "url"},
            "__locked__staging": True,
        },
    )
    rename_chain(store_path, "staging", "stage")
    store = load_store(store_path)
    assert store.get("__locked__stage") is True
    assert "__locked__staging" not in store


def test_rename_persists_to_disk(store_path):
    write_store(store_path, {"old": {"FOO": "bar"}})
    rename_chain(store_path, "old", "new")
    # Reload from disk
    store = load_store(store_path)
    assert "new" in store
    assert "old" not in store
