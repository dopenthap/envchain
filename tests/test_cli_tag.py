import pytest
from click.testing import CliRunner
from envchain.cli_tag import tag_cmd
from envchain.storage import save_store
from unittest.mock import patch


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def store(tmp_path):
    p = tmp_path / "store.json"
    save_store(p, {"prod": {"KEY": "val"}, "dev": {"KEY": "dev"}})
    return p


def test_add_tag(runner, store):
    with patch("envchain.cli_tag.get_store_path", return_value=store):
        result = runner.invoke(tag_cmd, ["add", "prod", "production"])
    assert result.exit_code == 0
    assert "Tagged 'prod' with 'production'" in result.output


def test_add_tag_missing_chain(runner, store):
    with patch("envchain.cli_tag.get_store_path", return_value=store):
        result = runner.invoke(tag_cmd, ["add", "ghost", "mytag"])
    assert result.exit_code == 1
    assert "Error" in result.output


def test_remove_tag(runner, store):
    with patch("envchain.cli_tag.get_store_path", return_value=store):
        runner.invoke(tag_cmd, ["add", "prod", "aws"])
        result = runner.invoke(tag_cmd, ["remove", "prod", "aws"])
    assert result.exit_code == 0
    assert "Removed" in result.output


def test_list_tags(runner, store):
    with patch("envchain.cli_tag.get_store_path", return_value=store):
        runner.invoke(tag_cmd, ["add", "prod", "live"])
        result = runner.invoke(tag_cmd, ["list", "prod"])
    assert "live" in result.output


def test_list_tags_empty(runner, store):
    with patch("envchain.cli_tag.get_store_path", return_value=store):
        result = runner.invoke(tag_cmd, ["list", "prod"])
    assert "No tags" in result.output


def test_find_by_tag(runner, store):
    with patch("envchain.cli_tag.get_store_path", return_value=store):
        runner.invoke(tag_cmd, ["add", "prod", "aws"])
        runner.invoke(tag_cmd, ["add", "dev", "aws"])
        result = runner.invoke(tag_cmd, ["find", "aws"])
    assert "prod" in result.output
    assert "dev" in result.output


def test_find_no_match(runner, store):
    with patch("envchain.cli_tag.get_store_path", return_value=store):
        result = runner.invoke(tag_cmd, ["find", "nope"])
    assert "No chains" in result.output
