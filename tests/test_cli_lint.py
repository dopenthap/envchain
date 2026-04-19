import json
import pytest
from click.testing import CliRunner
from envchain.cli_lint import lint_cmd


@pytest.fixture
def runner():
    return CliRunner()


def write_store(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def test_lint_no_issues(runner, tmp_path):
    p = tmp_path / "store.json"
    write_store(p, {"prod": {"API_KEY": "abc"}})
    result = runner.invoke(lint_cmd, ["--store", str(p)])
    assert result.exit_code == 0
    assert "No issues found" in result.output


def test_lint_empty_value(runner, tmp_path):
    p = tmp_path / "store.json"
    write_store(p, {"prod": {"API_KEY": ""}})
    result = runner.invoke(lint_cmd, ["--store", str(p)])
    assert result.exit_code == 1
    assert "empty value" in result.output


def test_lint_lowercase_key(runner, tmp_path):
    p = tmp_path / "store.json"
    write_store(p, {"prod": {"api_key": "val"}})
    result = runner.invoke(lint_cmd, ["--store", str(p)])
    assert result.exit_code == 1
    assert "not uppercase" in result.output


def test_lint_filter_by_chain(runner, tmp_path):
    p = tmp_path / "store.json"
    write_store(p, {
        "prod": {"bad_key": "val"},
        "dev": {"OTHER_BAD": ""},
    })
    result = runner.invoke(lint_cmd, ["--store", str(p), "prod"])
    assert "prod" in result.output
    assert "dev" not in result.output


def test_lint_missing_store(runner, tmp_path):
    p = tmp_path / "nofile.json"
    result = runner.invoke(lint_cmd, ["--store", str(p)])
    assert result.exit_code == 0
    assert "No issues found" in result.output
