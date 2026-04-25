"""Tests for envchain.hook."""

import pytest
from pathlib import Path

from envchain.hook import set_hook, remove_hook, get_hook, list_hooks, HookError
from envchain.storage import save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store({"mychain": {"KEY": "val"}}, store_path)
    return store_path


def test_set_and_get_hook(populated):
    set_hook("mychain", "post_activate", "echo activated", populated)
    assert get_hook("mychain", "post_activate", populated) == "echo activated"


def test_get_hook_not_set_returns_none(populated):
    assert get_hook("mychain", "pre_activate", populated) is None


def test_set_hook_missing_chain_raises(populated):
    with pytest.raises(HookError, match="not found"):
        set_hook("ghost", "post_activate", "echo hi", populated)


def test_set_hook_invalid_event_raises(populated):
    with pytest.raises(HookError, match="Unknown event"):
        set_hook("mychain", "on_explode", "echo boom", populated)


def test_remove_hook(populated):
    set_hook("mychain", "pre_activate", "echo pre", populated)
    remove_hook("mychain", "pre_activate", populated)
    assert get_hook("mychain", "pre_activate", populated) is None


def test_remove_hook_not_set_raises(populated):
    with pytest.raises(HookError, match="No hook set"):
        remove_hook("mychain", "pre_activate", populated)


def test_remove_hook_invalid_event_raises(populated):
    with pytest.raises(HookError, match="Unknown event"):
        remove_hook("mychain", "bad_event", populated)


def test_list_hooks_returns_all_set(populated):
    set_hook("mychain", "pre_activate", "echo pre", populated)
    set_hook("mychain", "post_deactivate", "echo post-deact", populated)
    hooks = list_hooks("mychain", populated)
    assert hooks == {
        "pre_activate": "echo pre",
        "post_deactivate": "echo post-deact",
    }


def test_list_hooks_missing_chain_raises(populated):
    with pytest.raises(HookError, match="not found"):
        list_hooks("ghost", populated)


def test_list_hooks_empty(populated):
    assert list_hooks("mychain", populated) == {}
