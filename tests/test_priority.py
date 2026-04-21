import pytest
from pathlib import Path
from envchain.priority import (
    set_priority,
    get_priority,
    remove_priority,
    list_by_priority,
    PriorityError,
)
from envchain.storage import save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {
        "prod": {"DB": "prod-db"},
        "staging": {"DB": "staging-db"},
        "dev": {"DB": "dev-db"},
    })
    return store_path


def test_set_and_get_priority(populated):
    set_priority(populated, "prod", 1)
    assert get_priority(populated, "prod") == 1


def test_get_priority_not_set_returns_none(populated):
    assert get_priority(populated, "dev") is None


def test_set_priority_missing_chain_raises(populated):
    with pytest.raises(PriorityError, match="not found"):
        set_priority(populated, "ghost", 5)


def test_set_priority_negative_raises(populated):
    with pytest.raises(PriorityError, match="non-negative"):
        set_priority(populated, "prod", -1)


def test_remove_priority(populated):
    set_priority(populated, "staging", 2)
    remove_priority(populated, "staging")
    assert get_priority(populated, "staging") is None


def test_remove_priority_not_set_raises(populated):
    with pytest.raises(PriorityError, match="no priority"):
        remove_priority(populated, "dev")


def test_remove_priority_missing_chain_raises(populated):
    with pytest.raises(PriorityError, match="not found"):
        remove_priority(populated, "ghost")


def test_list_by_priority_sorted(populated):
    set_priority(populated, "staging", 2)
    set_priority(populated, "prod", 1)
    result = list_by_priority(populated)
    names = [r[0] for r in result]
    # prod (1) before staging (2) before dev (None)
    assert names.index("prod") < names.index("staging")
    assert names.index("staging") < names.index("dev")


def test_list_by_priority_none_last(populated):
    set_priority(populated, "prod", 10)
    result = list_by_priority(populated)
    with_priority = [(n, p) for n, p in result if p is not None]
    without_priority = [(n, p) for n, p in result if p is None]
    assert all(result.index(a) < result.index(b)
               for a in with_priority for b in without_priority)


def test_list_by_priority_all_none(populated):
    result = list_by_priority(populated)
    assert all(p is None for _, p in result)
    assert len(result) == 3
