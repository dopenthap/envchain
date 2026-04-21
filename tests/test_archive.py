import json
import pytest
from pathlib import Path
from envchain.archive import (
    export_archive,
    write_archive,
    import_archive,
    ArchiveError,
)
from envchain.storage import save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    data = {
        "prod": {"DB_URL": "postgres://prod", "SECRET": "abc"},
        "staging": {"DB_URL": "postgres://staging"},
    }
    save_store(store_path, data)
    return store_path


def test_export_archive_basic(populated):
    archive = export_archive(["prod"], populated)
    assert archive["version"] == 1
    assert "prod" in archive["chains"]
    assert archive["chains"]["prod"]["DB_URL"] == "postgres://prod"


def test_export_archive_missing_chain_raises(populated):
    with pytest.raises(ArchiveError, match="Chain not found"):
        export_archive(["ghost"], populated)


def test_write_and_import_archive(populated, tmp_path):
    dest = tmp_path / "backup" / "env.json"
    write_archive(["prod", "staging"], dest, populated)
    assert dest.exists()

    # import into a fresh store
    new_store = tmp_path / "new_store.json"
    imported = import_archive(dest, new_store)
    assert sorted(imported) == ["prod", "staging"]

    raw = json.loads(new_store.read_text())
    assert raw["prod"]["SECRET"] == "abc"


def test_import_archive_no_overwrite_raises(populated, tmp_path):
    dest = tmp_path / "env.json"
    write_archive(["prod"], dest, populated)
    with pytest.raises(ArchiveError, match="already exists"):
        import_archive(dest, populated, overwrite=False)


def test_import_archive_with_overwrite(populated, tmp_path):
    dest = tmp_path / "env.json"
    write_archive(["prod"], dest, populated)
    imported = import_archive(dest, populated, overwrite=True)
    assert "prod" in imported


def test_import_archive_only_filter(populated, tmp_path):
    dest = tmp_path / "env.json"
    write_archive(["prod", "staging"], dest, populated)

    new_store = tmp_path / "filtered.json"
    imported = import_archive(dest, new_store, only=["staging"])
    assert imported == ["staging"]
    raw = json.loads(new_store.read_text())
    assert "prod" not in raw


def test_import_archive_missing_file_raises(tmp_path, store_path):
    with pytest.raises(ArchiveError, match="not found"):
        import_archive(tmp_path / "ghost.json", store_path)


def test_import_archive_invalid_json_raises(tmp_path, store_path):
    bad = tmp_path / "bad.json"
    bad.write_text("not json{{")
    with pytest.raises(ArchiveError, match="Invalid archive"):
        import_archive(bad, store_path)
