"""Tests for envchain.status."""

import pytest
from pathlib import Path
from envchain.storage import save_store
from envchain.status import get_status, StatusError
from envchain.lock import lock_chain
from envchain.protect import protect_chain
from envchain.freeze import freeze_chain
from envchain.describe import set_description
from envchain.tag import add_tag


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {
        "mychain": {"API_KEY": "abc", "SECRET": "xyz"},
    })
    return store_path


def test_get_status_basic(populated):
    status = get_status("mychain", populated)
    assert status.name == "mychain"
    assert status.key_count == 2
    assert status.locked is False
    assert status.protected is False
    assert status.frozen is False
    assert status.description is None
    assert status.tags == []
    assert status.expiry is None
    assert status.expired is False


def test_get_status_missing_chain_raises(populated):
    with pytest.raises(StatusError, match="not found"):
        get_status("ghost", populated)


def test_get_status_locked(populated):
    lock_chain("mychain", populated)
    status = get_status("mychain", populated)
    assert status.locked is True


def test_get_status_protected(populated):
    protect_chain("mychain", populated)
    status = get_status("mychain", populated)
    assert status.protected is True


def test_get_status_frozen(populated):
    freeze_chain("mychain", populated)
    status = get_status("mychain", populated)
    assert status.frozen is True


def test_get_status_with_description(populated):
    set_description("mychain", "my cool chain", populated)
    status = get_status("mychain", populated)
    assert status.description == "my cool chain"


def test_get_status_with_tags(populated):
    add_tag("mychain", "prod", populated)
    add_tag("mychain", "aws", populated)
    status = get_status("mychain", populated)
    assert "prod" in status.tags
    assert "aws" in status.tags


def test_summary_contains_name(populated):
    status = get_status("mychain", populated)
    assert "mychain" in status.summary()


def test_summary_shows_flags(populated):
    lock_chain("mychain", populated)
    protect_chain("mychain", populated)
    status = get_status("mychain", populated)
    summary = status.summary()
    assert "locked" in summary
    assert "protected" in summary
