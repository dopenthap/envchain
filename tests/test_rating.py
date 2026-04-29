"""Tests for envchain.rating."""

import pytest
from pathlib import Path
from envchain.storage import save_store
from envchain.rating import (
    set_rating,
    get_rating,
    clear_rating,
    list_ratings,
    RatingError,
)


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {
        "prod": {"API_KEY": "abc"},
        "dev": {"API_KEY": "dev123"},
    })
    return store_path


def test_set_and_get_rating(populated):
    set_rating(populated, "prod", 5)
    assert get_rating(populated, "prod") == 5


def test_get_rating_not_set_returns_none(populated):
    assert get_rating(populated, "prod") is None


def test_set_rating_invalid_value_raises(populated):
    with pytest.raises(RatingError, match="between 1 and 5"):
        set_rating(populated, "prod", 0)
    with pytest.raises(RatingError, match="between 1 and 5"):
        set_rating(populated, "prod", 6)


def test_set_rating_missing_chain_raises(populated):
    with pytest.raises(RatingError, match="not found"):
        set_rating(populated, "ghost", 3)


def test_get_rating_missing_chain_raises(populated):
    with pytest.raises(RatingError, match="not found"):
        get_rating(populated, "ghost")


def test_clear_rating(populated):
    set_rating(populated, "dev", 3)
    clear_rating(populated, "dev")
    assert get_rating(populated, "dev") is None


def test_clear_rating_not_set_raises(populated):
    with pytest.raises(RatingError, match="no rating set"):
        clear_rating(populated, "prod")


def test_clear_rating_missing_chain_raises(populated):
    with pytest.raises(RatingError, match="not found"):
        clear_rating(populated, "ghost")


def test_list_ratings(populated):
    set_rating(populated, "prod", 5)
    set_rating(populated, "dev", 2)
    result = list_ratings(populated)
    assert result == {"prod": 5, "dev": 2}


def test_list_ratings_empty(populated):
    assert list_ratings(populated) == {}
