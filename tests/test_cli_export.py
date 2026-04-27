import pytest
from click.testing import CliRunner
from unittest.mock import patch
from envchain.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


SAMPLE_VARS = {"API_KEY": "secret", "DEBUG": "true"}


def test_export_bash(runner):
    with patch("envchain.cli.get_chain", return_value=SAMPLE_VARS):
        result = runner.invoke(cli, ["export", "mychain"])
    assert result.exit_code == 0
    assert 'export API_KEY="secret"' in result.output
    assert 'export DEBUG="true"' in result.output


def test_export_dotenv(runner):
    with patch("envchain.cli.get_chain", return_value=SAMPLE_VARS):
        result = runner.invoke(cli, ["export", "mychain", "--format", "dotenv"])
    assert result.exit_code == 0
    assert 'API_KEY="secret"' in result.output


def test_export_fish(runner):
    with patch("envchain.cli.get_chain", return_value=SAMPLE_VARS):
        result = runner.invoke(cli, ["export", "mychain", "--format", "fish"])
    assert result.exit_code == 0
    assert 'set -x API_KEY "secret"' in result.output


def test_export_with_prefix(runner):
    with patch("envchain.cli.get_chain", return_value={"TOKEN": "abc"}):
        result = runner.invoke(cli, ["export", "mychain", "--prefix", "APP"])
    assert result.exit_code == 0
    assert 'export APP_TOKEN="abc"' in result.output


def test_export_empty_chain(runner):
    with patch("envchain.cli.get_chain", return_value={}):
        result = runner.invoke(cli, ["export", "ghost"])
    assert "empty or does not exist" in result.output


def test_export_invalid_format(runner):
    with patch("envchain.cli.get_chain", return_value=SAMPLE_VARS):
        result = runner.invoke(cli, ["export", "mychain", "--format", "zsh"])
    assert result.exit_code != 0


def test_export_value_with_special_chars(runner):
    """Ensure values containing spaces or quotes are exported correctly."""
    special_vars = {"GREETING": 'hello world', "QUOTE": 'it\'s fine'}
    with patch("envchain.cli.get_chain", return_value=special_vars):
        result = runner.invoke(cli, ["export", "mychain"])
    assert result.exit_code == 0
    assert 'export GREETING="hello world"' in result.output
    assert "export QUOTE=" in result.output
