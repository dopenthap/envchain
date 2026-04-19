import pytest
from pathlib import Path
from envchain.snapshot import create_snapshot, restore_snapshot, list_snapshots, delete_snapshot, SnapshotError
from envchain.storage import save_store, load_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {"prod": {"KEY": "val1", "SECRET": "s3cr3t"}})
    return store_path


def test_create_snapshot_returns_label(populated):
    label = create_snapshot("prod", "v1", populated)
    assert label == "v1"


def test_create_snapshot_auto_label(populated):
    label = create_snapshot("prod", None, populated)
    assert label  # non-empty timestamp
    assert "T" in label


def test_create_snapshot_persists(populated):
    create_snapshot("prod", "v1", populated)
    assert "v1" in list_snapshots("prod", populated)


def test_create_snapshot_missing_chain(store_path):
    save_store(store_path, {})
    with pytest.raises(SnapshotError, match="not found"):
        create_snapshot("ghost", "v1", store_path)


def test_create_snapshot_duplicate_label(populated):
    create_snapshot("prod", "v1", populated)
    with pytest.raises(SnapshotError, match="already exists"):
        create_snapshot("prod", "v1", populated)


def test_restore_snapshot(populated):
    create_snapshot("prod", "backup", populated)
    store = load_store(populated)
    store["prod"]["KEY"] = "changed"
    save_store(populated, store)
    restore_snapshot("prod", "backup", populated, overwrite=True)
    assert load_store(populated)["prod"]["KEY"] == "val1"


def test_restore_snapshot_no_overwrite_raises(populated):
    create_snapshot("prod", "backup", populated)
    with pytest.raises(SnapshotError, match="already exists"):
        restore_snapshot("prod", "backup", populated, overwrite=False)


def test_restore_snapshot_missing(populated):
    with pytest.raises(SnapshotError, match="not found"):
        restore_snapshot("prod", "nope", populated)


def test_list_snapshots_empty(populated):
    assert list_snapshots("prod", populated) == []


def test_list_snapshots_multiple(populated):
    create_snapshot("prod", "a", populated)
    create_snapshot("prod", "b", populated)
    assert list_snapshots("prod", populated) == ["a", "b"]


def test_delete_snapshot(populated):
    create_snapshot("prod", "v1", populated)
    delete_snapshot("prod", "v1", populated)
    assert "v1" not in list_snapshots("prod", populated)


def test_delete_snapshot_missing(populated):
    with pytest.raises(SnapshotError, match="not found"):
        delete_snapshot("prod", "ghost", populated)
