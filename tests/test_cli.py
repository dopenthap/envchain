import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from envchain.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_set_var(runner):
    with patch("envchain.cli.get_chain", return_value={}), \
         patch("envchain.cli.set_chain") as mock_set:
        result = runner.invoke(cli, ["set", "mychain", "FOO", "bar"])
        assert result.exit_code == 0
        assert "Set FOO in chain 'mychain'" in result.output
        mock_set.assert_called_once_with("mychain", {"FOO": "bar"})


def test_set_var_merges_existing(runner):
    with patch("envchain.cli.get_chain", return_value={"EXISTING": "val"}), \
         patch("envchain.cli.set_chain") as mock_set:
        runner.invoke(cli, ["set", "mychain", "FOO", "bar"])
        mock_set.assert_called_once_with("mychain", {"EXISTING": "val", "FOO": "bar"})


def test_get_var_single_key(runner):
    with patch("envchain.cli.get_chain", return_value={"FOO": "bar"}):
        result = runner.invoke(cli, ["get", "mychain", "FOO"])
        assert result.exit_code == 0
        assert result.output.strip() == "bar"


def test_get_var_all(runner):
    with patch("envchain.cli.get_chain", return_value={"A": "1", "B": "2"}):
        result = runner.invoke(cli, ["get", "mychain"])
        assert result.exit_code == 0
        assert "A=1" in result.output
        assert "B=2" in result.output


def test_get_chain_not_found(runner):
    with patch("envchain.cli.get_chain", return_value=None):
        result = runner.invoke(cli, ["get", "missing"])
        assert result.exit_code == 1


def test_list_chains(runner):
    with patch("envchain.cli.list_chains", return_value=["dev", "prod"]):
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "dev" in result.output
        assert "prod" in result.output


def test_list_chains_empty(runner):
    with patch("envchain.cli.list_chains", return_value=[]):
        result = runner.invoke(cli, ["list"])
        assert "No chains defined" in result.output


def test_delete_chain_with_yes(runner):
    with patch("envchain.cli.delete_chain", return_value=True) as mock_del:
        result = runner.invoke(cli, ["delete", "mychain", "--yes"])
        assert result.exit_code == 0
        assert "deleted" in result.output
        mock_del.assert_called_once_with("mychain")


def test_delete_chain_not_found(runner):
    with patch("envchain.cli.delete_chain", return_value=False):
        result = runner.invoke(cli, ["delete", "missing", "--yes"])
        assert result.exit_code == 1
