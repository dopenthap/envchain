"""Tests for envchain.label."""

import json
import pytest
from pathlib import Path
from envchain.label import LabelError, set_label, get_label, clear_label, list_labels


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


def write_store(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def test_set_and_get_label(store_path):
    write_store(store_path, {"prod": {"DB": "postgres"}})
    set_label(store_path, "prod", "Production")
    assert get_label(store_path, "prod") == "Production"


def test_get_label_not_set_returns_none(store_path):
    write_store(store_path, {"prod": {"DB": "postgres"}})
    assert get_label(store_path, "prod") is None


def test_set_label_missing_chain_raises(store_path):
    write_store(store_path, {})
    with pytest.raises(LabelError, match="not found"):
        set_label(store_path, "ghost", "Ghost")


def test_get_label_missing_chain_raises(store_path):
    write_store(store_path, {})
    with pytest.raises(LabelError, match="not found"):
        get_label(store_path, "ghost")


def test_set_label_empty_raises(store_path):
    write_store(store_path, {"prod": {}})
    with pytest.raises(LabelError, match="empty"):
        set_label(store_path, "prod", "   ")


def test_set_label_strips_whitespace(store_path):
    write_store(store_path, {"prod": {}})
    set_label(store_path, "prod", "  Staging  ")
    assert get_label(store_path, "prod") == "Staging"


def test_clear_label(store_path):
    write_store(store_path, {"prod": {}})
    set_label(store_path, "prod", "Production")
    clear_label(store_path, "prod")
    assert get_label(store_path, "prod") is None


def test_clear_label_not_set_raises(store_path):
    write_store(store_path, {"prod": {}})
    with pytest.raises(LabelError, match="no label"):
        clear_label(store_path, "prod")


def test_list_labels(store_path):
    write_store(store_path, {"prod": {}, "dev": {}, "staging": {}})
    set_label(store_path, "prod", "Production")
    set_label(store_path, "dev", "Development")
    labels = list_labels(store_path)
    assert labels == {"prod": "Production", "dev": "Development"}


def test_list_labels_excludes_deleted_chains(store_path):
    write_store(store_path, {"__label__orphan": {"value": "Orphan"}})
    labels = list_labels(store_path)
    assert "orphan" not in labels
