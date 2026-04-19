import pytest
from click.testing import CliRunner
from envchain.storage import save_store
from envchain.cli_lock import lock_cmd


@pytest.fixture
def runner(tmp_path, monkeypatch):
    store = tmp_path / "store.json"
    save_store(store, {"chains": {"prod": {"K": "v"}, "dev": {"X": "1"}}})
    monkeypatch.setattr("envchain.cli_lock.get_store_path", lambda: store)
    return CliRunner(), store


def test_lock_add(runner):
    r, _ = runner
    result = r.invoke(lock_cmd, ["add", "prod"])
    assert result.exit_code == 0
    assert "Locked chain 'prod'" in result.output


def test_lock_remove(runner):
    r, store = runner
    from envchain.lock import lock_chain
    lock_chain(store, "prod")
    result = r.invoke(lock_cmd, ["remove", "prod"])
    assert result.exit_code == 0
    assert "Unlocked chain 'prod'" in result.output


def test_lock_add_missing_chain(runner):
    r, _ = runner
    result = r.invoke(lock_cmd, ["add", "ghost"])
    assert result.exit_code == 1
    assert "Error" in result.output


def test_lock_remove_not_locked(runner):
    r, _ = runner
    result = r.invoke(lock_cmd, ["remove", "prod"])
    assert result.exit_code == 1
    assert "Error" in result.output


def test_lock_list_empty(runner):
    r, _ = runner
    result = r.invoke(lock_cmd, ["list"])
    assert result.exit_code == 0
    assert "No locked chains" in result.output


def test_lock_list_shows_locked(runner):
    r, store = runner
    from envchain.lock import lock_chain
    lock_chain(store, "prod")
    lock_chain(store, "dev")
    result = r.invoke(lock_cmd, ["list"])
    assert "prod" in result.output
    assert "dev" in result.output
