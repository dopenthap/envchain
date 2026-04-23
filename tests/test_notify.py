"""Tests for envchain.notify."""

import pytest

from envchain.notify import (
    NotifyError,
    get_notify,
    list_notify,
    remove_notify,
    set_notify,
)


@pytest.fixture()
def store():
    return {"mychain": {"KEY": "val"}}


def test_set_and_get_notify(store):
    set_notify(store, "mychain", "activate", "echo activated")
    assert get_notify(store, "mychain", "activate") == "echo activated"


def test_set_deactivate_hook(store):
    set_notify(store, "mychain", "deactivate", "echo bye")
    assert get_notify(store, "mychain", "deactivate") == "echo bye"


def test_get_notify_not_set_returns_none(store):
    assert get_notify(store, "mychain", "activate") is None


def test_set_notify_missing_chain_raises():
    store: dict = {}
    with pytest.raises(NotifyError, match="not found"):
        set_notify(store, "ghost", "activate", "echo hi")


def test_set_notify_invalid_event_raises(store):
    with pytest.raises(NotifyError, match="Unknown event"):
        set_notify(store, "mychain", "explode", "rm -rf /")


def test_remove_notify(store):
    set_notify(store, "mychain", "activate", "echo activated")
    remove_notify(store, "mychain", "activate")
    assert get_notify(store, "mychain", "activate") is None


def test_remove_notify_not_set_raises(store):
    with pytest.raises(NotifyError, match="No 'activate' hook"):
        remove_notify(store, "mychain", "activate")


def test_remove_notify_invalid_event_raises(store):
    with pytest.raises(NotifyError, match="Unknown event"):
        remove_notify(store, "mychain", "explode")


def test_list_notify_empty(store):
    assert list_notify(store, "mychain") == {}


def test_list_notify_multiple(store):
    set_notify(store, "mychain", "activate", "echo on")
    set_notify(store, "mychain", "deactivate", "echo off")
    result = list_notify(store, "mychain")
    assert result == {"activate": "echo on", "deactivate": "echo off"}


def test_remove_one_hook_keeps_other(store):
    set_notify(store, "mychain", "activate", "echo on")
    set_notify(store, "mychain", "deactivate", "echo off")
    remove_notify(store, "mychain", "activate")
    assert get_notify(store, "mychain", "activate") is None
    assert get_notify(store, "mychain", "deactivate") == "echo off"
