import pytest
from pathlib import Path
from envchain.history import (
    load_history,
    save_history,
    record_activation,
    get_last_chain,
    list_history,
)


@pytest.fixture
def history_path(tmp_path):
    return tmp_path / "history.json"


def test_load_history_missing_file(history_path):
    assert load_history(history_path) == {}


def test_save_and_load(history_path):
    save_history({"myproject": "prod"}, history_path)
    assert load_history(history_path) == {"myproject": "prod"}


def test_save_creates_parent_dirs(tmp_path):
    path = tmp_path / "nested" / "dir" / "history.json"
    save_history({"x": "y"}, path)
    assert path.exists()


def test_record_activation(history_path):
    record_activation("proj", "staging", history_path)
    assert get_last_chain("proj", history_path) == "staging"


def test_record_activation_overwrites(history_path):
    record_activation("proj", "staging", history_path)
    record_activation("proj", "prod", history_path)
    assert get_last_chain("proj", history_path) == "prod"


def test_get_last_chain_missing(history_path):
    assert get_last_chain("unknown", history_path) is None


def test_multiple_projects(history_path):
    record_activation("alpha", "dev", history_path)
    record_activation("beta", "prod", history_path)
    data = list_history(history_path)
    assert data["alpha"] == "dev"
    assert data["beta"] == "prod"


def test_list_history_empty(history_path):
    assert list_history(history_path) == {}
