"""Tests for the TTL CLI commands."""

import pytest
from click.testing import CliRunner

from envchain.cli_ttl import ttl_cmd
from envchain.storage import get_store_path, save_store


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def store(tmp_path, monkeypatch):
    path = tmp_path / "store.json"
    save_store(path, {"dev": {"API_KEY": "abc"}, "prod": {"API_KEY": "xyz"}})
    monkeypatch.setattr("envchain.cli_ttl.get_store_path", lambda: path)
    monkeypatch.setattr("envchain.ttl.get_store_path", lambda: path)
    return path


def test_set_ttl(runner, store):
    result = runner.invoke(ttl_cmd, ["set", "dev", "300"])
    assert result.exit_code == 0
    assert "expires in 300s" in result.output


def test_set_ttl_missing_chain(runner, store):
    result = runner.invoke(ttl_cmd, ["set", "ghost", "60"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_set_ttl_invalid_seconds(runner, store):
    result = runner.invoke(ttl_cmd, ["set", "dev", "0"])
    assert result.exit_code != 0
    assert "positive" in result.output


def test_remove_ttl(runner, store):
    runner.invoke(ttl_cmd, ["set", "dev", "100"])
    result = runner.invoke(ttl_cmd, ["remove", "dev"])
    assert result.exit_code == 0
    assert "removed" in result.output


def test_remove_ttl_not_set(runner, store):
    result = runner.invoke(ttl_cmd, ["remove", "dev"])
    assert result.exit_code != 0
    assert "no TTL set" in result.output


def test_show_ttl(runner, store):
    runner.invoke(ttl_cmd, ["set", "dev", "600"])
    result = runner.invoke(ttl_cmd, ["show", "dev"])
    assert result.exit_code == 0
    assert "600" in result.output
    assert "active" in result.output


def test_show_ttl_not_set(runner, store):
    result = runner.invoke(ttl_cmd, ["show", "dev"])
    assert result.exit_code == 0
    assert "No TTL set" in result.output


def test_list_ttls(runner, store):
    runner.invoke(ttl_cmd, ["set", "dev", "60"])
    runner.invoke(ttl_cmd, ["set", "prod", "120"])
    result = runner.invoke(ttl_cmd, ["list"])
    assert result.exit_code == 0
    assert "dev: 60s" in result.output
    assert "prod: 120s" in result.output


def test_list_ttls_empty(runner, store):
    result = runner.invoke(ttl_cmd, ["list"])
    assert result.exit_code == 0
    assert "No TTLs configured" in result.output
