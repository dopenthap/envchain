"""Tests for CLI status commands."""

import pytest
from click.testing import CliRunner
from envchain.cli_status import status_cmd
from envchain.storage import save_store
from envchain.lock import lock_chain
from envchain.tag import add_tag


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def store(tmp_path):
    p = tmp_path / "store.json"
    save_store(p, {
        "alpha": {"KEY": "val1", "OTHER": "val2"},
        "beta": {"TOKEN": "secret"},
    })
    return p


def test_show_basic(runner, store):
    result = runner.invoke(status_cmd, ["show", "alpha", "--store", str(store)])
    assert result.exit_code == 0
    assert "alpha" in result.output
    assert "keys" in result.output


def test_show_missing_chain(runner, store):
    result = runner.invoke(status_cmd, ["show", "ghost", "--store", str(store)])
    assert result.exit_code == 1
    assert "error" in result.output


def test_show_locked_flag(runner, store):
    lock_chain("alpha", store)
    result = runner.invoke(status_cmd, ["show", "alpha", "--store", str(store)])
    assert result.exit_code == 0
    assert "locked" in result.output


def test_list_all_chains(runner, store):
    result = runner.invoke(status_cmd, ["list", "--store", str(store)])
    assert result.exit_code == 0
    assert "alpha" in result.output
    assert "beta" in result.output


def test_list_shows_key_count(runner, store):
    result = runner.invoke(status_cmd, ["list", "--store", str(store)])
    assert "keys=2" in result.output
    assert "keys=1" in result.output


def test_list_shows_lock_flag(runner, store):
    lock_chain("beta", store)
    result = runner.invoke(status_cmd, ["list", "--store", str(store)])
    assert "[L]" in result.output


def test_list_shows_tags(runner, store):
    add_tag("alpha", "production", store)
    result = runner.invoke(status_cmd, ["list", "--store", str(store)])
    assert "production" in result.output


def test_list_empty_store(runner, tmp_path):
    p = tmp_path / "empty.json"
    save_store(p, {})
    result = runner.invoke(status_cmd, ["list", "--store", str(p)])
    assert result.exit_code == 0
    assert "no chains found" in result.output
