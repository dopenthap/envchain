import pytest
from click.testing import CliRunner
from envchain.cli_protect import protect_cmd
from envchain.storage import save_store, get_store_path
from unittest.mock import patch
from pathlib import Path


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def store(tmp_path):
    path = tmp_path / "store.json"
    save_store(path, {"prod": {"API_KEY": "secret"}, "dev": {"API_KEY": "dev-val"}})
    return path


def test_protect_add(runner, store):
    with patch("envchain.cli_protect.get_store_path", return_value=store):
        result = runner.invoke(protect_cmd, ["add", "prod"])
    assert result.exit_code == 0
    assert "protected" in result.output


def test_protect_add_missing_chain(runner, store):
    with patch("envchain.cli_protect.get_store_path", return_value=store):
        result = runner.invoke(protect_cmd, ["add", "ghost"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_protect_remove(runner, store):
    with patch("envchain.cli_protect.get_store_path", return_value=store):
        runner.invoke(protect_cmd, ["add", "prod"])
        result = runner.invoke(protect_cmd, ["remove", "prod"])
    assert result.exit_code == 0
    assert "no longer protected" in result.output


def test_protect_remove_not_protected(runner, store):
    with patch("envchain.cli_protect.get_store_path", return_value=store):
        result = runner.invoke(protect_cmd, ["remove", "dev"])
    assert result.exit_code != 0
    assert "is not protected" in result.output


def test_protect_list_empty(runner, store):
    with patch("envchain.cli_protect.get_store_path", return_value=store):
        result = runner.invoke(protect_cmd, ["list"])
    assert result.exit_code == 0
    assert "no protected chains" in result.output


def test_protect_list_shows_chains(runner, store):
    with patch("envchain.cli_protect.get_store_path", return_value=store):
        runner.invoke(protect_cmd, ["add", "prod"])
        result = runner.invoke(protect_cmd, ["list"])
    assert result.exit_code == 0
    assert "prod" in result.output
