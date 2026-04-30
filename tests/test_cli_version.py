import pytest
from click.testing import CliRunner
from envchain.storage import save_store
from envchain.cli_version import version_cmd


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def store(tmp_path, monkeypatch):
    path = tmp_path / "store.json"
    save_store(path, {"prod": {"API_KEY": "secret"}, "dev": {"API_KEY": "dev-key"}})
    monkeypatch.setattr("envchain.cli_version.get_store_path", lambda: path)
    monkeypatch.setattr("envchain.version.get_store_path", lambda: path)
    return path


def test_bump_version(runner, store):
    result = runner.invoke(version_cmd, ["bump", "prod"])
    assert result.exit_code == 0
    assert "version: 1" in result.output


def test_bump_version_increments(runner, store):
    runner.invoke(version_cmd, ["bump", "prod"])
    result = runner.invoke(version_cmd, ["bump", "prod"])
    assert "version: 2" in result.output


def test_bump_version_missing_chain(runner, store):
    result = runner.invoke(version_cmd, ["bump", "ghost"])
    assert result.exit_code == 1
    assert "error" in result.output


def test_get_version_default(runner, store):
    result = runner.invoke(version_cmd, ["get", "prod"])
    assert result.exit_code == 0
    assert result.output.strip() == "0"


def test_get_version_after_bump(runner, store):
    runner.invoke(version_cmd, ["bump", "prod"])
    runner.invoke(version_cmd, ["bump", "prod"])
    result = runner.invoke(version_cmd, ["get", "prod"])
    assert result.output.strip() == "2"


def test_get_version_missing_chain(runner, store):
    result = runner.invoke(version_cmd, ["get", "ghost"])
    assert result.exit_code == 1


def test_reset_version(runner, store):
    runner.invoke(version_cmd, ["bump", "prod"])
    result = runner.invoke(version_cmd, ["reset", "prod"])
    assert result.exit_code == 0
    assert "reset" in result.output
    get_result = runner.invoke(version_cmd, ["get", "prod"])
    assert get_result.output.strip() == "0"


def test_reset_version_missing_chain(runner, store):
    result = runner.invoke(version_cmd, ["reset", "ghost"])
    assert result.exit_code == 1


def test_list_versions_empty(runner, store):
    result = runner.invoke(version_cmd, ["list"])
    assert result.exit_code == 0
    assert "no versioned chains" in result.output


def test_list_versions(runner, store):
    runner.invoke(version_cmd, ["bump", "prod"])
    runner.invoke(version_cmd, ["bump", "dev"])
    runner.invoke(version_cmd, ["bump", "dev"])
    result = runner.invoke(version_cmd, ["list"])
    assert "prod" in result.output
    assert "dev" in result.output
    assert "1" in result.output
    assert "2" in result.output
