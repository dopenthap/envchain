import json
import pytest
from pathlib import Path
from envchain.search import search_chains, SearchError


@pytest.fixture
def store_path(tmp_path):
    p = tmp_path / "store.json"
    data = {
        "chains": {
            "prod": {"DB_HOST": "db.prod.example.com", "API_KEY": "secret123", "PORT": "5432"},
            "staging": {"DB_HOST": "db.staging.example.com", "DEBUG": "true"},
            "local": {"db_host": "localhost", "PORT": "3000"},
        }
    }
    p.write_text(json.dumps(data))
    return p


def test_search_keys_basic(store_path):
    results = search_chains(store_path, "DB_HOST")
    chains = {r.chain for r in results}
    assert chains == {"prod", "staging"}


def test_search_keys_partial(store_path):
    results = search_chains(store_path, "PORT")
    assert len(results) == 2


def test_search_values(store_path):
    results = search_chains(store_path, "staging", search_keys=False, search_values=True)
    assert len(results) == 2  # DB_HOST in prod and staging contain 'staging'
    assert all(r.chain in {"prod", "staging"} for r in results)


def test_search_keys_and_values(store_path):
    results = search_chains(store_path, "debug", search_keys=True, search_values=True, ignore_case=True)
    keys = {r.key for r in results}
    assert "DEBUG" in keys


def test_search_ignore_case(store_path):
    results = search_chains(store_path, "db_host", ignore_case=True)
    assert len(results) == 3


def test_search_chain_filter(store_path):
    results = search_chains(store_path, "DB_HOST", chain_filter="prod")
    assert len(results) == 1
    assert results[0].chain == "prod"


def test_search_no_match(store_path):
    results = search_chains(store_path, "NONEXISTENT")
    assert results == []


def test_search_invalid_pattern(store_path):
    with pytest.raises(SearchError, match="Invalid pattern"):
        search_chains(store_path, "[unclosed")


def test_results_sorted(store_path):
    results = search_chains(store_path, ".*")
    pairs = [(r.chain, r.key) for r in results]
    assert pairs == sorted(pairs)
