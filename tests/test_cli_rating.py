"""Tests for the rating CLI commands."""

import pytest
from click.testing import CliRunner
from envchain.storage import save_store, get_store_path
from envchain.cli_rating import rating_cmd


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def store(tmp_path, monkeypatch):
    path = tmp_path / "store.json"
    save_store(path, {
        "prod": {"KEY": "val"},
        "dev": {"KEY": "devval"},
    })
    monkeypatch.setattr("envchain.cli_rating.get_store_path", lambda: path)
    return path


def test_set_rating(runner, store):
    result = runner.invoke(rating_cmd, ["set", "prod", "4"])
    assert result.exit_code == 0
    assert "prod" in result.output
    assert "4/5" in result.output


def test_set_rating_invalid(runner, store):
    result = runner.invoke(rating_cmd, ["set", "prod", "7"])
    assert result.exit_code != 0
    assert "between 1 and 5" in result.output


def test_set_rating_missing_chain(runner, store):
    result = runner.invoke(rating_cmd, ["set", "ghost", "3"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_get_rating_not_set(runner, store):
    result = runner.invoke(rating_cmd, ["get", "prod"])
    assert result.exit_code == 0
    assert "No rating set" in result.output


def test_get_rating_set(runner, store):
    runner.invoke(rating_cmd, ["set", "prod", "5"])
    result = runner.invoke(rating_cmd, ["get", "prod"])
    assert result.exit_code == 0
    assert "5/5" in result.output


def test_clear_rating(runner, store):
    runner.invoke(rating_cmd, ["set", "dev", "2"])
    result = runner.invoke(rating_cmd, ["clear", "dev"])
    assert result.exit_code == 0
    assert "cleared" in result.output


def test_clear_rating_not_set(runner, store):
    result = runner.invoke(rating_cmd, ["clear", "prod"])
    assert result.exit_code != 0
    assert "no rating set" in result.output


def test_list_ratings(runner, store):
    runner.invoke(rating_cmd, ["set", "prod", "5"])
    runner.invoke(rating_cmd, ["set", "dev", "3"])
    result = runner.invoke(rating_cmd, ["list"])
    assert result.exit_code == 0
    assert "prod" in result.output
    assert "dev" in result.output


def test_list_ratings_empty(runner, store):
    result = runner.invoke(rating_cmd, ["list"])
    assert result.exit_code == 0
    assert "No chains" in result.output
