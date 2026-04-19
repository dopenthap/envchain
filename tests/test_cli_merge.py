import pytest
from click.testing import CliRunner
from unittest.mock import patch

from envchain.cli_merge import merge_cmd


@pytest.fixture
def runner():
    return CliRunner()


def test_merge_success(runner):
    merged = {"A": "1", "B": "2"}
    with patch("envchain.cli_merge.merge_chains", return_value=merged) as mock_merge:
        result = runner.invoke(merge_cmd, ["src", "dst", "myproject"])
    assert result.exit_code == 0
    assert "Merged 'src' into 'dst'" in result.output
    assert "A=1" in result.output
    assert "B=2" in result.output
    mock_merge.assert_called_once_with("src", "dst", "myproject", overwrite=False)


def test_merge_with_overwrite_flag(runner):
    merged = {"X": "99"}
    with patch("envchain.cli_merge.merge_chains", return_value=merged) as mock_merge:
        result = runner.invoke(merge_cmd, ["src", "dst", "myproject", "--overwrite"])
    assert result.exit_code == 0
    mock_merge.assert_called_once_with("src", "dst", "myproject", overwrite=True)


def test_merge_missing_chain_error(runner):
    from envchain.merge import ChainNotFoundError
    with patch(
        "envchain.cli_merge.merge_chains",
        side_effect=ChainNotFoundError("Source chain 'src' not found."),
    ):
        result = runner.invoke(merge_cmd, ["src", "dst", "myproject"])
    assert result.exit_code != 0
    assert "Source chain 'src' not found." in result.output


def test_merge_output_sorted_keys(runner):
    merged = {"Z": "last", "A": "first", "M": "mid"}
    with patch("envchain.cli_merge.merge_chains", return_value=merged):
        result = runner.invoke(merge_cmd, ["s", "d", "p"])
    lines = [l.strip() for l in result.output.splitlines() if "=" in l]
    keys = [l.split("=")[0] for l in lines]
    assert keys == sorted(keys)
