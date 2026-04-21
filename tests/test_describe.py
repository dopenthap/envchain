import json
import pytest
from pathlib import Path
from envchain.describe import (
    set_description,
    get_description,
    clear_description,
    list_descriptions,
    DescribeError,
)


@pytest.fixture
def store_path(tmp_path):
    p = tmp_path / "store.json"
    data = {
        "prod": {"API_KEY": "secret"},
        "dev": {"DEBUG": "1"},
    }
    p.write_text(json.dumps(data))
    return p


def test_set_and_get_description(store_path):
    set_description(store_path, "prod", "Production environment")
    desc = get_description(store_path, "prod")
    assert desc == "Production environment"


def test_get_description_not_set_returns_none(store_path):
    desc = get_description(store_path, "dev")
    assert desc is None


def test_set_description_missing_chain_raises(store_path):
    with pytest.raises(DescribeError, match="not found"):
        set_description(store_path, "staging", "Staging env")


def test_get_description_missing_chain_raises(store_path):
    with pytest.raises(DescribeError, match="not found"):
        get_description(store_path, "ghost")


def test_clear_description(store_path):
    set_description(store_path, "prod", "To be removed")
    clear_description(store_path, "prod")
    assert get_description(store_path, "prod") is None


def test_clear_description_not_set_is_noop(store_path):
    # should not raise
    clear_description(store_path, "dev")
    assert get_description(store_path, "dev") is None


def test_clear_description_missing_chain_raises(store_path):
    with pytest.raises(DescribeError, match="not found"):
        clear_description(store_path, "nope")


def test_list_descriptions(store_path):
    set_description(store_path, "prod", "Prod desc")
    set_description(store_path, "dev", "Dev desc")
    result = list_descriptions(store_path)
    assert result == {"prod": "Prod desc", "dev": "Dev desc"}


def test_list_descriptions_empty(store_path):
    result = list_descriptions(store_path)
    assert result == {}


def test_description_persists_across_loads(store_path):
    set_description(store_path, "prod", "Persistent")
    raw = json.loads(store_path.read_text())
    assert raw.get("__meta__.prod.description") == "Persistent"
