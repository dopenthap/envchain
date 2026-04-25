import pytest
from pathlib import Path
from envchain.quota import (
    set_quota, remove_quota, get_quota, check_quota, list_quotas, QuotaError
)
from envchain.storage import save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {
        "dev": {"API_KEY": "abc", "DB_URL": "postgres://localhost"},
        "prod": {"API_KEY": "xyz"},
    })
    return store_path


def test_set_and_get_quota(populated):
    set_quota(populated, "dev", 5)
    assert get_quota(populated, "dev") == 5


def test_get_quota_not_set_returns_none(populated):
    assert get_quota(populated, "dev") is None


def test_set_quota_missing_chain_raises(populated):
    with pytest.raises(QuotaError, match="not found"):
        set_quota(populated, "ghost", 3)


def test_set_quota_zero_raises(populated):
    with pytest.raises(QuotaError, match="at least 1"):
        set_quota(populated, "dev", 0)


def test_remove_quota(populated):
    set_quota(populated, "dev", 5)
    remove_quota(populated, "dev")
    assert get_quota(populated, "dev") is None


def test_remove_quota_not_set_raises(populated):
    with pytest.raises(QuotaError, match="No quota set"):
        remove_quota(populated, "dev")


def test_check_quota_under_limit(populated):
    set_quota(populated, "dev", 5)
    check_quota(populated, "dev")  # dev has 2 keys, limit 5 — should not raise


def test_check_quota_at_limit_raises(populated):
    set_quota(populated, "dev", 2)  # dev has exactly 2 keys
    with pytest.raises(QuotaError, match="reached its quota"):
        check_quota(populated, "dev")


def test_check_quota_no_quota_set_passes(populated):
    check_quota(populated, "dev")  # no quota, should pass silently


def test_check_quota_missing_chain_raises(populated):
    with pytest.raises(QuotaError, match="not found"):
        check_quota(populated, "ghost")


def test_list_quotas(populated):
    set_quota(populated, "dev", 10)
    set_quota(populated, "prod", 3)
    result = list_quotas(populated)
    assert result == {"dev": 10, "prod": 3}


def test_list_quotas_empty(populated):
    assert list_quotas(populated) == {}
