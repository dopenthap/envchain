import pytest
from pathlib import Path
from envchain.import_ import import_from_text, import_from_file, ImportError
from envchain.storage import load_store, save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


def test_import_basic(store_path):
    result = import_from_text("FOO=bar\nBAZ=qux\n", "mychain", store_path=store_path)
    assert result == {"FOO": "bar", "BAZ": "qux"}


def test_import_persists(store_path):
    import_from_text("FOO=bar", "mychain", store_path=store_path)
    store = load_store(store_path)
    assert store["chains"]["mychain"]["FOO"] == "bar"


def test_import_strips_export_keyword(store_path):
    result = import_from_text("export FOO=bar\nexport BAZ=qux", "c", store_path=store_path)
    assert result == {"FOO": "bar", "BAZ": "qux"}


def test_import_strips_quotes(store_path):
    result = import_from_text('FOO="hello world"\nBAR=\'single\'', "c", store_path=store_path)
    assert result["FOO"] == "hello world"
    assert result["BAR"] == "single"


def test_import_skips_comments_and_blanks(store_path):
    text = "# comment\n\nFOO=bar\n"
    result = import_from_text(text, "c", store_path=store_path)
    assert list(result.keys()) == ["FOO"]


def test_import_no_overwrite_keeps_existing(store_path):
    save_store(store_path, {"chains": {"c": {"FOO": "original"}}})
    import_from_text("FOO=new\nBAR=added", "c", overwrite=False, store_path=store_path)
    store = load_store(store_path)
    assert store["chains"]["c"]["FOO"] == "original"
    assert store["chains"]["c"]["BAR"] == "added"


def test_import_overwrite_replaces_existing(store_path):
    save_store(store_path, {"chains": {"c": {"FOO": "original"}}})
    import_from_text("FOO=new", "c", overwrite=True, store_path=store_path)
    store = load_store(store_path)
    assert store["chains"]["c"]["FOO"] == "new"


def test_import_empty_raises(store_path):
    with pytest.raises(ImportError, match="No valid"):
        import_from_text("# just a comment\n", "c", store_path=store_path)


def test_import_from_file(tmp_path, store_path):
    f = tmp_path / ".env"
    f.write_text("KEY=value\n")
    result = import_from_file(f, "c", store_path=store_path)
    assert result["KEY"] == "value"


def test_import_from_file_missing(tmp_path, store_path):
    with pytest.raises(ImportError, match="File not found"):
        import_from_file(tmp_path / "nope.env", "c", store_path=store_path)
