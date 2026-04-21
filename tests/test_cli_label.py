"""Tests for label CLI commands."""

import json
import pytest
from click.testing import CliRunner
from envchain.cli_label import label_cmd


@pytest.fixture
def runner():
    return CliRunner()


def _store(tmp_path, data):
    p = tmp_path / "store.json"
    p.write_text(json.dumps(data))
    return p


def test_set_label(runner, tmp_path, monkeypatch):
    p = _store(tmp_path, {"prod": {}})
    monkeypatch.setattr("envchain.cli_label.get_store_path", lambda: p)
    result = runner.invoke(label_cmd, ["set", "prod", "Production"])
    assert result.exit_code == 0
    assert "Production" in result.output


def test_set_label_missing_chain(runner, tmp_path, monkeypatch):
    p = _store(tmp_path, {})
    monkeypatch.setattr("envchain.cli_label.get_store_path", lambda: p)
    result = runner.invoke(label_cmd, ["set", "ghost", "Ghost"])
    assert result.exit_code != 0
    assert "not found" in result.output


def test_get_label(runner, tmp_path, monkeypatch):
    p = _store(tmp_path, {"prod": {}, "__label__prod": {"value": "Production"}})
    monkeypatch.setattr("envchain.cli_label.get_store_path", lambda: p)
    result = runner.invoke(label_cmd, ["get", "prod"])
    assert result.exit_code == 0
    assert "Production" in result.output


def test_get_label_not_set(runner, tmp_path, monkeypatch):
    p = _store(tmp_path, {"prod": {}})
    monkeypatch.setattr("envchain.cli_label.get_store_path", lambda: p)
    result = runner.invoke(label_cmd, ["get", "prod"])
    assert result.exit_code == 0
    assert "No label" in result.output


def test_clear_label(runner, tmp_path, monkeypatch):
    p = _store(tmp_path, {"prod": {}, "__label__prod": {"value": "Production"}})
    monkeypatch.setattr("envchain.cli_label.get_store_path", lambda: p)
    result = runner.invoke(label_cmd, ["clear", "prod"])
    assert result.exit_code == 0
    assert "cleared" in result.output


def test_list_labels(runner, tmp_path, monkeypatch):
    p = _store(tmp_path, {
        "prod": {},
        "dev": {},
        "__label__prod": {"value": "Production"},
        "__label__dev": {"value": "Development"},
    })
    monkeypatch.setattr("envchain.cli_label.get_store_path", lambda: p)
    result = runner.invoke(label_cmd, ["list"])
    assert result.exit_code == 0
    assert "prod: Production" in result.output
    assert "dev: Development" in result.output


def test_list_labels_empty(runner, tmp_path, monkeypatch):
    p = _store(tmp_path, {})
    monkeypatch.setattr("envchain.cli_label.get_store_path", lambda: p)
    result = runner.invoke(label_cmd, ["list"])
    assert result.exit_code == 0
    assert "No labels" in result.output
