"""Tests for envchain.audit."""

import pytest
from pathlib import Path
from envchain.audit import record_event, load_events, clear_events


@pytest.fixture
def audit_path(tmp_path):
    return tmp_path


def test_load_events_missing_file(audit_path):
    events = load_events(audit_path)
    assert events == []


def test_record_and_load(audit_path):
    record_event("set", "mychain", "FOO", audit_path)
    events = load_events(audit_path)
    assert len(events) == 1
    assert events[0]["action"] == "set"
    assert events[0]["chain"] == "mychain"
    assert events[0]["detail"] == "FOO"
    assert "ts" in events[0]


def test_multiple_events(audit_path):
    record_event("set", "chain1", "A", audit_path)
    record_event("delete", "chain1", "A", audit_path)
    record_event("activate", "chain2", "", audit_path)
    events = load_events(audit_path)
    assert len(events) == 3
    assert events[1]["action"] == "delete"


def test_clear_events(audit_path):
    record_event("set", "x", "Y", audit_path)
    clear_events(audit_path)
    assert load_events(audit_path) == []


def test_creates_parent_dirs(tmp_path):
    deep = tmp_path / "a" / "b"
    record_event("set", "c", "D", deep)
    events = load_events(deep)
    assert len(events) == 1


def test_empty_detail_allowed(audit_path):
    record_event("activate", "prod", audit_path=audit_path)
    events = load_events(audit_path)
    assert events[0]["detail"] == ""
