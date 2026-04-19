import json
import pytest
from pathlib import Path
from envchain.lint import lint_store, LintWarning


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


def write_store(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def test_empty_value_warning(store_path):
    write_store(store_path, {"prod": {"API_KEY": ""}})
    warnings = lint_store(store_path)
    assert LintWarning("prod", "API_KEY", "empty value") in warnings


def test_lowercase_key_warning(store_path):
    write_store(store_path, {"prod": {"api_key": "secret"}})
    warnings = lint_store(store_path)
    assert LintWarning("prod", "api_key", "key is not uppercase") in warnings


def test_key_with_spaces_warning(store_path):
    write_store(store_path, {"prod": {"MY KEY": "value"}})
    warnings = lint_store(store_path)
    assert LintWarning("prod", "MY KEY", "key contains spaces") in warnings


def test_no_warnings_clean_chain(store_path):
    write_store(store_path, {"prod": {"API_KEY": "abc123", "SECRET": "xyz"}})
    warnings = lint_store(store_path)
    assert warnings == []


def test_duplicate_value_across_chains(store_path):
    write_store(store_path, {
        "prod": {"API_KEY": "shared_secret"},
        "staging": {"API_KEY": "shared_secret"},
    })
    warnings = lint_store(store_path)
    chains = {(w.chain, w.key) for w in warnings if w.message == "duplicate value shared across chains"}
    assert ("prod", "API_KEY") in chains
    assert ("staging", "API_KEY") in chains


def test_empty_store(store_path):
    write_store(store_path, {})
    assert lint_store(store_path) == []


def test_missing_store(store_path):
    # load_store returns {} for missing file
    warnings = lint_store(store_path)
    assert warnings == []
