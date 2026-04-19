import pytest
from pathlib import Path
from envchain.storage import save_store
from envchain.tag import add_tag, remove_tag, get_tags, find_by_tag, TagError


@pytest.fixture
def store_path(tmp_path):
    p = tmp_path / "store.json"
    save_store(p, {"prod": {"KEY": "val"}, "dev": {"KEY": "dev_val"}})
    return p


def test_add_tag(store_path):
    add_tag(store_path, "prod", "production")
    assert "production" in get_tags(store_path, "prod")


def test_add_tag_multiple(store_path):
    add_tag(store_path, "prod", "production")
    add_tag(store_path, "prod", "aws")
    tags = get_tags(store_path, "prod")
    assert "production" in tags
    assert "aws" in tags


def test_add_tag_deduplicates(store_path):
    add_tag(store_path, "prod", "production")
    add_tag(store_path, "prod", "production")
    assert get_tags(store_path, "prod").count("production") == 1


def test_add_tag_missing_chain(store_path):
    with pytest.raises(TagError, match="not found"):
        add_tag(store_path, "ghost", "mytag")


def test_remove_tag(store_path):
    add_tag(store_path, "prod", "production")
    remove_tag(store_path, "prod", "production")
    assert "production" not in get_tags(store_path, "prod")


def test_remove_tag_not_present(store_path):
    with pytest.raises(TagError, match="not found"):
        remove_tag(store_path, "prod", "nonexistent")


def test_get_tags_empty(store_path):
    assert get_tags(store_path, "prod") == []


def test_find_by_tag(store_path):
    add_tag(store_path, "prod", "aws")
    add_tag(store_path, "dev", "aws")
    result = find_by_tag(store_path, "aws")
    assert result == ["dev", "prod"]


def test_find_by_tag_no_match(store_path):
    assert find_by_tag(store_path, "nonexistent") == []
