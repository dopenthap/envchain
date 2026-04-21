import pytest
from envchain.note import NoteError, set_note, get_note, clear_note, list_notes
from envchain.storage import save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store({"prod": {"KEY": "val"}, "dev": {"KEY": "devval"}}, store_path)
    return store_path


def test_set_and_get_note(populated):
    set_note("prod", "Production secrets — handle with care.", populated)
    assert get_note("prod", populated) == "Production secrets — handle with care."


def test_get_note_not_set_returns_none(populated):
    assert get_note("dev", populated) is None


def test_set_note_missing_chain_raises(populated):
    with pytest.raises(NoteError, match="not found"):
        set_note("staging", "some note", populated)


def test_get_note_missing_chain_raises(populated):
    with pytest.raises(NoteError, match="not found"):
        get_note("staging", populated)


def test_clear_note_removes_note(populated):
    set_note("prod", "temporary note", populated)
    clear_note("prod", populated)
    assert get_note("prod", populated) is None


def test_clear_note_noop_when_not_set(populated):
    # should not raise
    clear_note("dev", populated)
    assert get_note("dev", populated) is None


def test_clear_note_missing_chain_raises(populated):
    with pytest.raises(NoteError, match="not found"):
        clear_note("ghost", populated)


def test_list_notes(populated):
    set_note("prod", "note for prod", populated)
    set_note("dev", "note for dev", populated)
    notes = list_notes(populated)
    assert notes == {"prod": "note for prod", "dev": "note for dev"}


def test_list_notes_empty(populated):
    assert list_notes(populated) == {}


def test_set_note_overwrites_existing(populated):
    set_note("prod", "first", populated)
    set_note("prod", "second", populated)
    assert get_note("prod", populated) == "second"
