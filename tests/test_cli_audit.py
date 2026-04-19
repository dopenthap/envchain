"""Tests for audit CLI commands."""

import pytest
from click.testing import CliRunner
from envchain.cli_audit import audit_cmd
from envchain.audit import record_event, get_audit_path
from pathlib import Path
import envchain.audit as audit_module


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def patch_audit_path(tmp_path, monkeypatch):
    audit_file = tmp_path / "audit.log"
    monkeypatch.setattr(audit_module, "AUDIT_FILE", audit_file)


def test_log_empty(runner):
    result = runner.invoke(audit_cmd, ["log"])
    assert result.exit_code == 0
    assert "No audit entries found" in result.output


def test_log_shows_entries(runner):
    record_event("set", "prod", "API_KEY")
    result = runner.invoke(audit_cmd, ["log"])
    assert result.exit_code == 0
    assert "set" in result.output
    assert "prod" in result.output


def test_log_filter_by_chain(runner):
    record_event("set", "prod", "A")
    record_event("set", "dev", "B")
    result = runner.invoke(audit_cmd, ["log", "--chain", "dev"])
    assert "dev" in result.output
    assert "prod" not in result.output


def test_log_filter_by_action(runner):
    record_event("set", "prod", "A")
    record_event("delete", "prod", "A")
    result = runner.invoke(audit_cmd, ["log", "--action", "delete"])
    assert "delete" in result.output


def test_clear_cmd(runner):
    record_event("set", "prod", "X")
    result = runner.invoke(audit_cmd, ["clear"], input="y\n")
    assert result.exit_code == 0
    assert "cleared" in result.output


def test_path_cmd(runner):
    result = runner.invoke(audit_cmd, ["path"])
    assert result.exit_code == 0
    assert "audit.log" in result.output
