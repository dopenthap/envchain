import pytest
from pathlib import Path
from envchain.storage import save_store
from envchain.badge import BadgeError, set_badge, get_badge, clear_badge, list_badges


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {
        "prod": {"API_KEY": "abc"},
        "staging": {"API_KEY": "xyz"},
    })
    return store_path


def test_set_and_get_badge(populated):
    set_badge(populated, "prod", "🚀 live")
    assert get_badge(populated, "prod") == "🚀 live"


def test_get_badge_not_set_returns_none(populated):
    assert get_badge(populated, "prod") is None


def test_set_badge_strips_whitespace(populated):
    set_badge(populated, "prod", "  beta  ")
    assert get_badge(populated, "prod") == "beta"


def test_set_badge_missing_chain_raises(populated):
    with pytest.raises(BadgeError, match="not found"):
        set_badge(populated, "ghost", "nope")


def test_set_badge_empty_raises(populated):
    with pytest.raises(BadgeError, match="must not be empty"):
        set_badge(populated, "prod", "   ")


def test_set_badge_too_long_raises(populated):
    with pytest.raises(BadgeError, match="32 characters"):
        set_badge(populated, "prod", "x" * 33)


def test_clear_badge(populated):
    set_badge(populated, "prod", "v1")
    clear_badge(populated, "prod")
    assert get_badge(populated, "prod") is None


def test_clear_badge_not_set_raises(populated):
    with pytest.raises(BadgeError, match="no badge set"):
        clear_badge(populated, "prod")


def test_clear_badge_missing_chain_raises(populated):
    with pytest.raises(BadgeError, match="not found"):
        clear_badge(populated, "ghost")


def test_list_badges(populated):
    set_badge(populated, "prod", "live")
    set_badge(populated, "staging", "wip")
    badges = list_badges(populated)
    assert badges == {"prod": "live", "staging": "wip"}


def test_list_badges_empty(populated):
    assert list_badges(populated) == {}
