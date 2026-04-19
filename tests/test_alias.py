import pytest
from pathlib import Path
from envchain.alias import set_alias, remove_alias, resolve_alias, list_aliases, AliasError
from envchain.storage import save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {"chains": {"prod": {"KEY": "val"}, "staging": {"KEY": "stg"}}})
    return store_path


def test_set_alias(populated):
    set_alias(populated, "p", "prod")
    assert list_aliases(populated) == {"p": "prod"}


def test_set_alias_missing_chain(populated):
    with pytest.raises(AliasError, match="does not exist"):
        set_alias(populated, "x", "nope")


def test_set_alias_reserved_name(populated):
    with pytest.raises(AliasError, match="reserved"):
        set_alias(populated, "__meta__", "prod")


def test_remove_alias(populated):
    set_alias(populated, "p", "prod")
    remove_alias(populated, "p")
    assert list_aliases(populated) == {}


def test_remove_alias_not_found(populated):
    with pytest.raises(AliasError, match="not found"):
        remove_alias(populated, "ghost")


def test_resolve_alias(populated):
    set_alias(populated, "p", "prod")
    assert resolve_alias(populated, "p") == "prod"


def test_resolve_non_alias(populated):
    assert resolve_alias(populated, "prod") == "prod"


def test_list_aliases_empty(populated):
    assert list_aliases(populated) == {}


def test_list_aliases_multiple(populated):
    set_alias(populated, "p", "prod")
    set_alias(populated, "s", "staging")
    result = list_aliases(populated)
    assert result == {"p": "prod", "s": "staging"}
