import pytest
from click.testing import CliRunner
from unittest.mock import patch
from envchain.diff_cli import diff_cmd


@pytest.fixture
def runner():
    return CliRunner()


SAMPLE_STORE = {
    "chains": {
        "dev": {"FOO": "1", "BAR": "old"},
        "prod": {"FOO": "1", "BAR": "new", "EXTRA": "x"},
    }
}


def test_diff_changed_key(runner):
    with patch("envchain.diff_cli.load_store", return_value=SAMPLE_STORE):
        result = runner.invoke(diff_cmd, ["dev", "prod"])
    assert result.exit_code == 0
    assert "~ BAR" in result.output


def test_diff_only_in_b(runner):
    with patch("envchain.diff_cli.load_store", return_value=SAMPLE_STORE):
        result = runner.invoke(diff_cmd, ["dev", "prod"])
    assert "> EXTRA" in result.output


def test_diff_no_differences(runner):
    store = {"chains": {"a": {"K": "v"}, "b": {"K": "v"}}}
    with patch("envchain.diff_cli.load_store", return_value=store):
        result = runner.invoke(diff_cmd, ["a", "b"])
    assert result.exit_code == 0
    assert "No differences" in result.output


def test_diff_missing_chain_error(runner):
    with patch("envchain.diff_cli.load_store", return_value=SAMPLE_STORE):
        result = runner.invoke(diff_cmd, ["dev", "ghost"])
    assert result.exit_code != 0
    assert "Chain not found" in result.output
