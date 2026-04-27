"""Tests for CLI region commands."""

import pytest
from click.testing import CliRunner

from envchain.cli_region import region_cmd
from envchain.storage import get_store_path, save_store


@pytest.fixture()
def runner(tmp_path, monkeypatch):
    monkeypatch.setenv("ENVCHAIN_STORE", str(tmp_path / "store.json"))
    save_store(
        get_store_path(),
        {"alpha": {"A": "1"}, "beta": {"B": "2"}},
    )
    return CliRunner()


def test_set_region(runner):
    result = runner.invoke(region_cmd, ["set", "alpha", "prod"])
    assert result.exit_code == 0
    assert "prod" in result.output


def test_set_region_invalid(runner):
    result = runner.invoke(region_cmd, ["set", "alpha", "moon"])
    assert result.exit_code != 0
    assert "Invalid region" in result.output


def test_set_region_missing_chain(runner):
    result = runner.invoke(region_cmd, ["set", "ghost", "dev"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_get_region_not_set(runner):
    result = runner.invoke(region_cmd, ["get", "alpha"])
    assert result.exit_code == 0
    assert "No region" in result.output


def test_get_region_after_set(runner):
    runner.invoke(region_cmd, ["set", "alpha", "staging"])
    result = runner.invoke(region_cmd, ["get", "alpha"])
    assert result.exit_code == 0
    assert "staging" in result.output


def test_clear_region(runner):
    runner.invoke(region_cmd, ["set", "alpha", "dev"])
    result = runner.invoke(region_cmd, ["clear", "alpha"])
    assert result.exit_code == 0
    assert "cleared" in result.output


def test_clear_region_not_set(runner):
    result = runner.invoke(region_cmd, ["clear", "alpha"])
    assert result.exit_code != 0
    assert "no region set" in result.output


def test_list_by_region(runner):
    runner.invoke(region_cmd, ["set", "alpha", "prod"])
    runner.invoke(region_cmd, ["set", "beta", "prod"])
    result = runner.invoke(region_cmd, ["list", "prod"])
    assert result.exit_code == 0
    assert "alpha" in result.output
    assert "beta" in result.output


def test_list_by_region_empty(runner):
    result = runner.invoke(region_cmd, ["list", "test"])
    assert result.exit_code == 0
    assert "No chains" in result.output
