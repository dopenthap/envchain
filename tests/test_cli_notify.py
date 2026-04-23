"""CLI tests for notify commands."""

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from envchain.cli_notify import notify_cmd
from envchain.storage import save_store


@pytest.fixture()
def runner(tmp_path, monkeypatch):
    store_file = tmp_path / "store.json"
    monkeypatch.setenv("ENVCHAIN_STORE", str(store_file))
    save_store(store_file, {"prod": {"KEY": "val"}})
    return CliRunner()


def test_set_notify(runner):
    result = runner.invoke(notify_cmd, ["set", "prod", "activate", "echo hello"])
    assert result.exit_code == 0
    assert "Hook set" in result.output


def test_set_notify_missing_chain(runner):
    result = runner.invoke(notify_cmd, ["set", "ghost", "activate", "echo hi"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_remove_notify(runner):
    runner.invoke(notify_cmd, ["set", "prod", "activate", "echo on"])
    result = runner.invoke(notify_cmd, ["remove", "prod", "activate"])
    assert result.exit_code == 0
    assert "removed" in result.output


def test_remove_notify_not_set(runner):
    result = runner.invoke(notify_cmd, ["remove", "prod", "activate"])
    assert result.exit_code != 0
    assert "No 'activate' hook" in result.output


def test_show_specific_event(runner):
    runner.invoke(notify_cmd, ["set", "prod", "activate", "echo on"])
    result = runner.invoke(notify_cmd, ["show", "prod", "activate"])
    assert result.exit_code == 0
    assert "echo on" in result.output


def test_show_no_hooks(runner):
    result = runner.invoke(notify_cmd, ["show", "prod"])
    assert result.exit_code == 0
    assert "No hooks" in result.output


def test_show_all_hooks(runner):
    runner.invoke(notify_cmd, ["set", "prod", "activate", "echo on"])
    runner.invoke(notify_cmd, ["set", "prod", "deactivate", "echo off"])
    result = runner.invoke(notify_cmd, ["show", "prod"])
    assert result.exit_code == 0
    assert "activate" in result.output
    assert "deactivate" in result.output
