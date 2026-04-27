import pytest
from pathlib import Path
from envchain.storage import save_store
from envchain.visibility import (
    set_visibility,
    get_visibility,
    clear_visibility,
    list_by_visibility,
    VisibilityError,
)


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {
        "prod": {"DB_URL": "postgres://prod"},
        "staging": {"DB_URL": "postgres://staging"},
        "dev": {"DB_URL": "postgres://dev"},
    })
    return store_path


def test_set_and_get_visibility(populated):
    set_visibility(populated, "prod", "private")
    assert get_visibility(populated, "prod") == "private"


def test_get_visibility_not_set_returns_none(populated):
    assert get_visibility(populated, "dev") is None


def test_set_visibility_invalid_level_raises(populated):
    with pytest.raises(VisibilityError, match="Invalid visibility level"):
        set_visibility(populated, "prod", "secret")


def test_set_visibility_missing_chain_raises(populated):
    with pytest.raises(VisibilityError, match="not found"):
        set_visibility(populated, "ghost", "public")


def test_get_visibility_missing_chain_raises(populated):
    with pytest.raises(VisibilityError, match="not found"):
        get_visibility(populated, "ghost")


def test_clear_visibility(populated):
    set_visibility(populated, "staging", "internal")
    clear_visibility(populated, "staging")
    assert get_visibility(populated, "staging") is None


def test_clear_visibility_not_set_raises(populated):
    with pytest.raises(VisibilityError, match="no visibility set"):
        clear_visibility(populated, "dev")


def test_list_by_visibility(populated):
    set_visibility(populated, "prod", "private")
    set_visibility(populated, "staging", "private")
    set_visibility(populated, "dev", "public")
    assert list_by_visibility(populated, "private") == ["prod", "staging"]
    assert list_by_visibility(populated, "public") == ["dev"]
    assert list_by_visibility(populated, "internal") == []


def test_list_by_visibility_invalid_level_raises(populated):
    with pytest.raises(VisibilityError, match="Invalid visibility level"):
        list_by_visibility(populated, "unknown")
