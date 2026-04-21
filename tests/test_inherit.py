import pytest
from pathlib import Path
from envchain.storage import save_store
from envchain.inherit import (
    set_parent,
    remove_parent,
    get_parent,
    resolve_chain,
    InheritError,
)


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    data = {
        "base": {"HOST": "localhost", "PORT": "5432"},
        "dev": {"PORT": "5433", "DEBUG": "1"},
        "prod": {"HOST": "prod.example.com"},
    }
    save_store(store_path, data)
    return store_path


def test_set_and_get_parent(populated):
    set_parent("dev", "base", populated)
    assert get_parent("dev", populated) == "base"


def test_get_parent_not_set_returns_none(populated):
    assert get_parent("dev", populated) is None


def test_set_parent_missing_chain_raises(populated):
    with pytest.raises(InheritError, match="chain 'ghost' not found"):
        set_parent("ghost", "base", populated)


def test_set_parent_missing_parent_raises(populated):
    with pytest.raises(InheritError, match="parent chain 'ghost' not found"):
        set_parent("dev", "ghost", populated)


def test_set_parent_self_raises(populated):
    with pytest.raises(InheritError, match="cannot inherit from itself"):
        set_parent("dev", "dev", populated)


def test_set_parent_cycle_raises(populated):
    set_parent("dev", "base", populated)
    with pytest.raises(InheritError, match="cycle detected"):
        set_parent("base", "dev", populated)


def test_remove_parent(populated):
    set_parent("dev", "base", populated)
    remove_parent("dev", populated)
    assert get_parent("dev", populated) is None


def test_remove_parent_not_set_raises(populated):
    with pytest.raises(InheritError, match="has no parent set"):
        remove_parent("dev", populated)


def test_resolve_chain_merges_parent(populated):
    set_parent("dev", "base", populated)
    result = resolve_chain("dev", populated)
    # child PORT overrides parent PORT
    assert result["PORT"] == "5433"
    # parent HOST is inherited
    assert result["HOST"] == "localhost"
    # child-only key present
    assert result["DEBUG"] == "1"


def test_resolve_chain_no_parent(populated):
    result = resolve_chain("dev", populated)
    assert result == {"PORT": "5433", "DEBUG": "1"}


def test_resolve_chain_missing_chain_raises(populated):
    with pytest.raises(InheritError, match="chain 'ghost' not found"):
        resolve_chain("ghost", populated)
