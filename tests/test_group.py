import pytest
from pathlib import Path
from envchain.storage import save_store
from envchain.group import (
    create_group,
    get_group,
    delete_group,
    list_groups,
    add_to_group,
    remove_from_group,
    GroupError,
)


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


@pytest.fixture
def populated(store_path):
    save_store(store_path, {
        "dev": {"DB_URL": "postgres://localhost/dev"},
        "staging": {"DB_URL": "postgres://staging/db"},
        "prod": {"DB_URL": "postgres://prod/db"},
    })
    return store_path


def test_create_group(populated):
    create_group(populated, "envs", ["dev", "staging"])
    assert get_group(populated, "envs") == ["dev", "staging"]


def test_create_group_missing_chain_raises(populated):
    with pytest.raises(GroupError, match="Chain not found: ghost"):
        create_group(populated, "bad", ["dev", "ghost"])


def test_get_group_missing_raises(populated):
    with pytest.raises(GroupError, match="Group not found: nope"):
        get_group(populated, "nope")


def test_delete_group(populated):
    create_group(populated, "envs", ["dev", "staging"])
    delete_group(populated, "envs")
    with pytest.raises(GroupError):
        get_group(populated, "envs")


def test_delete_group_missing_raises(populated):
    with pytest.raises(GroupError, match="Group not found"):
        delete_group(populated, "nonexistent")


def test_list_groups(populated):
    create_group(populated, "envs", ["dev", "staging"])
    create_group(populated, "all", ["dev", "staging", "prod"])
    groups = list_groups(populated)
    assert set(groups.keys()) == {"envs", "all"}
    assert groups["envs"] == ["dev", "staging"]
    assert groups["all"] == ["dev", "staging", "prod"]


def test_list_groups_empty(populated):
    assert list_groups(populated) == {}


def test_add_to_group(populated):
    create_group(populated, "envs", ["dev"])
    add_to_group(populated, "envs", "staging")
    assert "staging" in get_group(populated, "envs")


def test_add_to_group_deduplicates(populated):
    create_group(populated, "envs", ["dev"])
    add_to_group(populated, "envs", "dev")
    assert get_group(populated, "envs").count("dev") == 1


def test_add_to_group_missing_chain_raises(populated):
    create_group(populated, "envs", ["dev"])
    with pytest.raises(GroupError, match="Chain not found"):
        add_to_group(populated, "envs", "ghost")


def test_remove_from_group(populated):
    create_group(populated, "envs", ["dev", "staging"])
    remove_from_group(populated, "envs", "staging")
    assert get_group(populated, "envs") == ["dev"]


def test_remove_from_group_not_member_raises(populated):
    create_group(populated, "envs", ["dev"])
    with pytest.raises(GroupError, match="not in group"):
        remove_from_group(populated, "envs", "prod")
