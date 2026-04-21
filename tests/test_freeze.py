import pytest
from pathlib import Path
from envchain.freeze import (
    freeze_chain,
    unfreeze_chain,
    is_frozen,
    assert_unfrozen,
    list_frozen,
    FreezeError,
)
from envchain.storage import save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {
        "dev": {"API_KEY": "abc"},
        "prod": {"API_KEY": "xyz"},
    })
    return store_path


def test_freeze_chain(populated):
    freeze_chain("dev", populated)
    assert is_frozen("dev", populated) is True


def test_freeze_missing_chain_raises(populated):
    with pytest.raises(FreezeError, match="not found"):
        freeze_chain("ghost", populated)


def test_freeze_already_frozen_raises(populated):
    freeze_chain("dev", populated)
    with pytest.raises(FreezeError, match="already frozen"):
        freeze_chain("dev", populated)


def test_unfreeze_chain(populated):
    freeze_chain("dev", populated)
    unfreeze_chain("dev", populated)
    assert is_frozen("dev", populated) is False


def test_unfreeze_not_frozen_raises(populated):
    with pytest.raises(FreezeError, match="not frozen"):
        unfreeze_chain("dev", populated)


def test_is_frozen_returns_false_by_default(populated):
    assert is_frozen("prod", populated) is False


def test_assert_unfrozen_passes_when_not_frozen(populated):
    assert_unfrozen("dev", populated)  # should not raise


def test_assert_unfrozen_raises_when_frozen(populated):
    freeze_chain("dev", populated)
    with pytest.raises(FreezeError, match="frozen and cannot be modified"):
        assert_unfrozen("dev", populated)


def test_list_frozen_empty(populated):
    assert list_frozen(populated) == []


def test_list_frozen_returns_sorted(populated):
    freeze_chain("prod", populated)
    freeze_chain("dev", populated)
    assert list_frozen(populated) == ["dev", "prod"]
