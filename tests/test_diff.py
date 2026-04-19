import pytest
from envchain.diff import diff_chains


def _setup():
    return {
        "chains": {
            "alpha": {"FOO": "1", "BAR": "2", "SHARED": "same"},
            "beta": {"BAZ": "3", "SHARED": "same", "FOO": "changed"},
            "empty": {},
        }
    }


def test_diff_only_in_a():
    data = _setup()
    result = diff_chains(data, "alpha", "beta")
    assert "BAR" in result["only_in_a"]


def test_diff_only_in_b():
    data = _setup()
    result = diff_chains(data, "alpha", "beta")
    assert "BAZ" in result["only_in_b"]


def test_diff_changed():
    data = _setup()
    result = diff_chains(data, "alpha", "beta")
    assert "FOO" in result["changed"]
    assert result["changed"]["FOO"]["a"] == "1"
    assert result["changed"]["FOO"]["b"] == "changed"


def test_diff_no_changes_for_shared():
    data = _setup()
    result = diff_chains(data, "alpha", "beta")
    assert "SHARED" not in result["changed"]
    assert "SHARED" not in result["only_in_a"]
    assert "SHARED" not in result["only_in_b"]


def test_diff_empty_chain():
    data = _setup()
    result = diff_chains(data, "alpha", "empty")
    assert set(result["only_in_a"]) == {"FOO", "BAR", "SHARED"}
    assert result["only_in_b"] == []
    assert result["changed"] == {}


def test_diff_missing_chain_raises():
    data = _setup()
    with pytest.raises(KeyError):
        diff_chains(data, "alpha", "nonexistent")
