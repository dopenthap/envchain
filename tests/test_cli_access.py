"""CLI tests for envchain access commands."""

import pytest
from click.testing import CliRunner

from envchain.storage import save_store
from envchain.cli_access import access_cmd


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def store(tmp_path, monkeypatch):
    path = tmp_path / "store.json"
    save_store(path, {"prod": {"KEY": "val"}, "dev": {"KEY": "devval"}})
    monkeypatch.setenv("ENVCHAIN_STORE", str(path))
    return path


def test_set_access(runner, store):
    result = runner.invoke(access_cmd, ["set", "prod", "alice", "bob"])
    assert result.exit_code == 0
    assert "alice" in result.output
    assert "bob" in result.output


def test_set_access_missing_chain(runner, store):
    result = runner.invoke(access_cmd, ["set", "ghost", "alice"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_remove_access(runner, store):
    runner.invoke(access_cmd, ["set", "prod", "alice"])
    result = runner.invoke(access_cmd, ["remove", "prod"])
    assert result.exit_code == 0
    assert "removed" in result.output


def test_remove_access_not_set(runner, store):
    result = runner.invoke(access_cmd, ["remove", "prod"])
    assert result.exit_code != 0
    assert "no access rules" in result.output


def test_show_unrestricted(runner, store):
    result = runner.invoke(access_cmd, ["show", "prod"])
    assert result.exit_code == 0
    assert "unrestricted" in result.output


def test_show_with_users(runner, store):
    runner.invoke(access_cmd, ["set", "prod", "alice", "carol"])
    result = runner.invoke(access_cmd, ["show", "prod"])
    assert result.exit_code == 0
    assert "alice" in result.output
    assert "carol" in result.output
