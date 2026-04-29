"""Tests for the owner CLI commands."""

import pytest
from click.testing import CliRunner

from envchain.cli_owner import owner_cmd
from envchain.storage import get_store_path, save_store


@pytest.fixture()
def runner():
    return CliRunner()


@pytest.fixture()
def store(tmp_path, monkeypatch):
    path = tmp_path / "store.json"
    save_store(path, {
        "prod": {"KEY": "val"},
        "dev": {"KEY": "devval"},
    })
    monkeypatch.setenv("ENVCHAIN_STORE", str(path))
    return path


def test_set_owner(runner, store):
    result = runner.invoke(owner_cmd, ["set", "prod", "alice"])
    assert result.exit_code == 0
    assert "alice" in result.output


def test_set_owner_missing_chain(runner, store):
    result = runner.invoke(owner_cmd, ["set", "ghost", "alice"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_get_owner(runner, store):
    runner.invoke(owner_cmd, ["set", "prod", "alice"])
    result = runner.invoke(owner_cmd, ["get", "prod"])
    assert result.exit_code == 0
    assert "alice" in result.output


def test_get_owner_not_set(runner, store):
    result = runner.invoke(owner_cmd, ["get", "prod"])
    assert result.exit_code == 0
    assert "No owner" in result.output


def test_get_owner_missing_chain(runner, store):
    result = runner.invoke(owner_cmd, ["get", "ghost"])
    assert result.exit_code != 0


def test_clear_owner(runner, store):
    runner.invoke(owner_cmd, ["set", "prod", "alice"])
    result = runner.invoke(owner_cmd, ["clear", "prod"])
    assert result.exit_code == 0
    assert "cleared" in result.output


def test_list_owners(runner, store):
    runner.invoke(owner_cmd, ["set", "prod", "alice"])
    runner.invoke(owner_cmd, ["set", "dev", "bob"])
    result = runner.invoke(owner_cmd, ["list"])
    assert result.exit_code == 0
    assert "prod" in result.output
    assert "alice" in result.output
    assert "dev" in result.output
    assert "bob" in result.output


def test_list_owners_empty(runner, store):
    result = runner.invoke(owner_cmd, ["list"])
    assert result.exit_code == 0
    assert "No owners" in result.output
