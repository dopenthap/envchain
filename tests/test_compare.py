import json
import pytest
from pathlib import Path
from envchain.compare import compare_chains, CompareError


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


def write_store(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def test_compare_only_in_a(store_path):
    write_store(store_path, {"chains": {
        "a": {"FOO": "1", "BAR": "2"},
        "b": {"BAR": "2"},
    }})
    result = compare_chains(store_path, "a", "b")
    assert result.only_in_a == ["FOO"]
    assert result.only_in_b == []


def test_compare_only_in_b(store_path):
    write_store(store_path, {"chains": {
        "a": {"BAR": "2"},
        "b": {"BAR": "2", "BAZ": "3"},
    }})
    result = compare_chains(store_path, "a", "b")
    assert result.only_in_b == ["BAZ"]
    assert result.only_in_a == []


def test_compare_shared_same(store_path):
    write_store(store_path, {"chains": {
        "a": {"KEY": "val"},
        "b": {"KEY": "val"},
    }})
    result = compare_chains(store_path, "a", "b")
    assert result.shared_same == ["KEY"]
    assert result.shared_different == []
    assert not result.has_differences()


def test_compare_shared_different(store_path):
    write_store(store_path, {"chains": {
        "a": {"KEY": "old"},
        "b": {"KEY": "new"},
    }})
    result = compare_chains(store_path, "a", "b")
    assert result.shared_different == ["KEY"]
    assert result.shared_same == []
    assert result.has_differences()


def test_compare_summary(store_path):
    write_store(store_path, {"chains": {
        "a": {"X": "1", "Y": "2", "Z": "same"},
        "b": {"Y": "changed", "Z": "same", "W": "new"},
    }})
    result = compare_chains(store_path, "a", "b")
    s = result.summary()
    assert s["only_in_a"] == 1
    assert s["only_in_b"] == 1
    assert s["shared_same"] == 1
    assert s["shared_different"] == 1


def test_compare_missing_chain_a(store_path):
    write_store(store_path, {"chains": {"b": {"K": "v"}}})
    with pytest.raises(CompareError, match="Chain not found: a"):
        compare_chains(store_path, "a", "b")


def test_compare_missing_chain_b(store_path):
    write_store(store_path, {"chains": {"a": {"K": "v"}}})
    with pytest.raises(CompareError, match="Chain not found: b"):
        compare_chains(store_path, "a", "b")
