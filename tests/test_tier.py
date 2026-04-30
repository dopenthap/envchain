import pytest
from pathlib import Path
from envchain.tier import set_tier, get_tier, clear_tier, list_tiers, TierError
from envchain.storage import save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {"mychain": {"KEY": "val"}, "other": {"X": "1"}})
    return store_path


def test_set_and_get_tier(populated):
    set_tier(populated, "mychain", "prod")
    assert get_tier(populated, "mychain") == "prod"


def test_set_tier_strips_and_lowercases(populated):
    set_tier(populated, "mychain", "  Dev  ")
    assert get_tier(populated, "mychain") == "dev"


def test_get_tier_not_set_returns_none(populated):
    assert get_tier(populated, "mychain") is None


def test_set_tier_invalid_raises(populated):
    with pytest.raises(TierError, match="Invalid tier"):
        set_tier(populated, "mychain", "enterprise")


def test_set_tier_missing_chain_raises(populated):
    with pytest.raises(TierError, match="not found"):
        set_tier(populated, "ghost", "dev")


def test_get_tier_missing_chain_raises(populated):
    with pytest.raises(TierError, match="not found"):
        get_tier(populated, "ghost")


def test_clear_tier(populated):
    set_tier(populated, "mychain", "staging")
    clear_tier(populated, "mychain")
    assert get_tier(populated, "mychain") is None


def test_clear_tier_not_set_raises(populated):
    with pytest.raises(TierError, match="no tier set"):
        clear_tier(populated, "mychain")


def test_clear_tier_missing_chain_raises(populated):
    with pytest.raises(TierError, match="not found"):
        clear_tier(populated, "ghost")


def test_list_tiers(populated):
    set_tier(populated, "mychain", "prod")
    set_tier(populated, "other", "dev")
    result = list_tiers(populated)
    assert result == {"mychain": "prod", "other": "dev"}


def test_list_tiers_empty(populated):
    assert list_tiers(populated) == {}
