import pytest
from pathlib import Path
from envchain.pin import pin_chain, unpin_chain, get_pin, list_pins, PinError
from envchain.storage import save_store
from envchain.snapshot import create_snapshot


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    store = {"mychain": {"KEY": "val"}, "other": {"X": "1"}}
    save_store(store_path, store)
    label = create_snapshot(store_path, "mychain", label="v1")
    return store_path


def test_pin_chain(populated):
    pin_chain(populated, "mychain", "v1")
    assert get_pin(populated, "mychain") == "v1"


def test_pin_missing_chain(populated):
    with pytest.raises(PinError, match="not found"):
        pin_chain(populated, "ghost", "v1")


def test_pin_missing_snapshot(populated):
    with pytest.raises(PinError, match="snapshot"):
        pin_chain(populated, "mychain", "nonexistent")


def test_unpin_chain(populated):
    pin_chain(populated, "mychain", "v1")
    unpin_chain(populated, "mychain")
    assert get_pin(populated, "mychain") is None


def test_unpin_not_pinned(populated):
    with pytest.raises(PinError, match="not pinned"):
        unpin_chain(populated, "mychain")


def test_list_pins(populated):
    pin_chain(populated, "mychain", "v1")
    pins = list_pins(populated)
    assert pins == {"mychain": "v1"}


def test_list_pins_empty(populated):
    assert list_pins(populated) == {}


def test_get_pin_none_when_absent(populated):
    assert get_pin(populated, "other") is None
