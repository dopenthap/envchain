import pytest
from envchain.color import (
    ColorError,
    set_color,
    get_color,
    clear_color,
    list_colors,
)


@pytest.fixture
def store():
    return {"prod": {"API_KEY": "abc"}, "dev": {"DEBUG": "1"}}


def test_set_and_get_color(store):
    set_color(store, "prod", "red")
    assert get_color(store, "prod") == "red"


def test_set_color_strips_and_lowercases(store):
    set_color(store, "prod", "  GREEN  ")
    assert get_color(store, "prod") == "green"


def test_get_color_not_set_returns_none(store):
    assert get_color(store, "prod") is None


def test_set_color_invalid_raises(store):
    with pytest.raises(ColorError, match="invalid color"):
        set_color(store, "prod", "purple")


def test_set_color_missing_chain_raises(store):
    with pytest.raises(ColorError, match="chain not found"):
        set_color(store, "staging", "blue")


def test_get_color_missing_chain_raises(store):
    with pytest.raises(ColorError, match="chain not found"):
        get_color(store, "staging")


def test_clear_color(store):
    set_color(store, "prod", "cyan")
    clear_color(store, "prod")
    assert get_color(store, "prod") is None


def test_clear_color_not_set_raises(store):
    with pytest.raises(ColorError, match="no color set"):
        clear_color(store, "prod")


def test_clear_color_missing_chain_raises(store):
    with pytest.raises(ColorError, match="chain not found"):
        clear_color(store, "ghost")


def test_list_colors(store):
    set_color(store, "prod", "red")
    set_color(store, "dev", "green")
    result = list_colors(store)
    assert result == {"prod": "red", "dev": "green"}


def test_list_colors_empty(store):
    assert list_colors(store) == {}


def test_color_none_is_valid(store):
    set_color(store, "prod", "none")
    assert get_color(store, "prod") == "none"
