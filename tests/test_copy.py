import pytest
from envchain.copy import copy_chain, rename_chain
from envchain.storage import load_store, save_store


@pytest.fixture
def store_path(tmp_path):
    path = tmp_path / "store.json"
    save_store(path, {
        "dev": {"DB_URL": "postgres://localhost/dev", "DEBUG": "true"},
        "prod": {"DB_URL": "postgres://prod-host/app"},
    })
    return path


def test_copy_chain_creates_dst(store_path):
    vars_ = copy_chain("dev", "staging", store_path=store_path)
    assert vars_ == {"DB_URL": "postgres://localhost/dev", "DEBUG": "true"}
    store = load_store(store_path)
    assert "staging" in store
    assert store["staging"] == store["dev"]


def test_copy_chain_does_not_mutate_src(store_path):
    copy_chain("dev", "staging", store_path=store_path)
    store = load_store(store_path)
    store["staging"]["NEW"] = "val"
    # src should be unaffected (we check original store reload)
    store2 = load_store(store_path)
    assert "NEW" not in store2["dev"]


def test_copy_chain_missing_src(store_path):
    with pytest.raises(KeyError, match="nope"):
        copy_chain("nope", "other", store_path=store_path)


def test_copy_chain_dst_exists_no_overwrite(store_path):
    with pytest.raises(ValueError, match="already exists"):
        copy_chain("dev", "prod", store_path=store_path)


def test_copy_chain_dst_exists_with_overwrite(store_path):
    vars_ = copy_chain("dev", "prod", store_path=store_path, overwrite=True)
    assert vars_["DEBUG"] == "true"
    store = load_store(store_path)
    assert store["prod"] == store["dev"]


def test_rename_chain(store_path):
    rename_chain("dev", "development", store_path=store_path)
    store = load_store(store_path)
    assert "development" in store
    assert "dev" not in store
    assert store["development"]["DEBUG"] == "true"


def test_rename_chain_dst_exists_no_overwrite(store_path):
    with pytest.raises(ValueError):
        rename_chain("dev", "prod", store_path=store_path)


def test_rename_chain_src_removed_on_overwrite(store_path):
    rename_chain("dev", "prod", store_path=store_path, overwrite=True)
    store = load_store(store_path)
    assert "dev" not in store
    assert store["prod"]["DEBUG"] == "true"
