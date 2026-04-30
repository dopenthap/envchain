import pytest
from pathlib import Path
from envchain.storage import save_store
from envchain.version import (
    VersionError,
    bump_version,
    get_version,
    reset_version,
    list_versions,
)


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {"mychain": {"KEY": "val"}, "other": {"X": "1"}})
    return store_path


def test_get_version_default_is_zero(populated):
    assert get_version(populated, "mychain") == 0


def test_bump_version_returns_new_version(populated):
    v = bump_version(populated, "mychain")
    assert v == 1


def test_bump_version_increments(populated):
    bump_version(populated, "mychain")
    bump_version(populated, "mychain")
    v = bump_version(populated, "mychain")
    assert v == 3


def test_get_version_after_bump(populated):
    bump_version(populated, "mychain")
    bump_version(populated, "mychain")
    assert get_version(populated, "mychain") == 2


def test_bump_version_missing_chain_raises(populated):
    with pytest.raises(VersionError, match="not found"):
        bump_version(populated, "ghost")


def test_get_version_missing_chain_raises(populated):
    with pytest.raises(VersionError, match="not found"):
        get_version(populated, "ghost")


def test_reset_version(populated):
    bump_version(populated, "mychain")
    bump_version(populated, "mychain")
    reset_version(populated, "mychain")
    assert get_version(populated, "mychain") == 0


def test_reset_version_missing_chain_raises(populated):
    with pytest.raises(VersionError, match="not found"):
        reset_version(populated, "ghost")


def test_list_versions_empty(populated):
    assert list_versions(populated) == {}


def test_list_versions_after_bumps(populated):
    bump_version(populated, "mychain")
    bump_version(populated, "other")
    bump_version(populated, "other")
    result = list_versions(populated)
    assert result == {"mychain": 1, "other": 2}


def test_versions_are_independent(populated):
    bump_version(populated, "mychain")
    bump_version(populated, "mychain")
    bump_version(populated, "other")
    assert get_version(populated, "mychain") == 2
    assert get_version(populated, "other") == 1
