"""CLI tests for hook commands."""

import pytest
from click.testing import CliRunner

from envchain.cli_hook import hook_cmd
from envchain.storage import save_store
from unittest.mock import patch


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def store(tmp_path):
    p = tmp_path / "store.json"
    save_store({"prod": {"API_KEY": "secret"}}, p)
    return p


def _invoke(runner, args, store):
    with patch("envchain.hook.get_store_path", return_value=store):
        return runner.invoke(hook_cmd, args)


def test_set_hook(runner, store):
    result = _invoke(runner, ["set", "prod", "post_activate", "echo hello"], store)
    assert result.exit_code == 0
    assert "Hook set" in result.output


def test_set_hook_missing_chain(runner, store):
    result = _invoke(runner, ["set", "ghost", "post_activate", "echo hi"], store)
    assert result.exit_code != 0
    assert "not found" in result.output


def test_remove_hook(runner, store):
    _invoke(runner, ["set", "prod", "pre_activate", "echo pre"], store)
    result = _invoke(runner, ["remove", "prod", "pre_activate"], store)
    assert result.exit_code == 0
    assert "removed" in result.output


def test_remove_hook_not_set(runner, store):
    result = _invoke(runner, ["remove", "prod", "pre_activate"], store)
    assert result.exit_code != 0
    assert "No hook set" in result.output


def test_show_hook(runner, store):
    _invoke(runner, ["set", "prod", "post_activate", "notify.sh"], store)
    result = _invoke(runner, ["show", "prod", "post_activate"], store)
    assert result.exit_code == 0
    assert "notify.sh" in result.output


def test_show_hook_not_set(runner, store):
    result = _invoke(runner, ["show", "prod", "post_activate"], store)
    assert result.exit_code == 0
    assert "No hook set" in result.output


def test_list_hooks(runner, store):
    _invoke(runner, ["set", "prod", "pre_activate", "echo pre"], store)
    _invoke(runner, ["set", "prod", "post_deactivate", "echo post"], store)
    result = _invoke(runner, ["list", "prod"], store)
    assert result.exit_code == 0
    assert "pre_activate" in result.output
    assert "post_deactivate" in result.output


def test_list_hooks_empty(runner, store):
    result = _invoke(runner, ["list", "prod"], store)
    assert result.exit_code == 0
    assert "No hooks" in result.output
