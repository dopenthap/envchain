import pytest
from envchain.promote import promote_chain, PromoteError
from envchain.storage import load_store, save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


def write_store(store_path, data):
    save_store(store_path, data)


def test_promote_all_keys(store_path):
    write_store(store_path, {
        "staging": {"DB_URL": "postgres://staging", "SECRET": "abc"},
        "prod": {"EXISTING": "yes"},
    })
    promoted = promote_chain(store_path, "staging", "prod")
    assert promoted == {"DB_URL": "postgres://staging", "SECRET": "abc"}
    store = load_store(store_path)
    assert store["prod"]["DB_URL"] == "postgres://staging"
    assert store["prod"]["EXISTING"] == "yes"


def test_promote_selected_keys(store_path):
    write_store(store_path, {
        "staging": {"DB_URL": "postgres://staging", "SECRET": "abc"},
        "prod": {},
    })
    promoted = promote_chain(store_path, "staging", "prod", keys=["DB_URL"])
    assert list(promoted.keys()) == ["DB_URL"]
    store = load_store(store_path)
    assert "SECRET" not in store["prod"]


def test_promote_with_prefix(store_path):
    write_store(store_path, {
        "base": {"TOKEN": "tok123"},
        "app": {},
    })
    promoted = promote_chain(store_path, "base", "app", prefix="APP_")
    assert "APP_TOKEN" in promoted
    store = load_store(store_path)
    assert store["app"]["APP_TOKEN"] == "tok123"


def test_promote_no_overwrite_raises(store_path):
    write_store(store_path, {
        "staging": {"KEY": "new_val"},
        "prod": {"KEY": "old_val"},
    })
    with pytest.raises(PromoteError, match="already exists"):
        promote_chain(store_path, "staging", "prod")


def test_promote_with_overwrite(store_path):
    write_store(store_path, {
        "staging": {"KEY": "new_val"},
        "prod": {"KEY": "old_val"},
    })
    promote_chain(store_path, "staging", "prod", overwrite=True)
    store = load_store(store_path)
    assert store["prod"]["KEY"] == "new_val"


def test_promote_missing_src_raises(store_path):
    write_store(store_path, {"prod": {}})
    with pytest.raises(PromoteError, match="source chain"):
        promote_chain(store_path, "staging", "prod")


def test_promote_missing_dst_raises(store_path):
    write_store(store_path, {"staging": {"K": "v"}})
    with pytest.raises(PromoteError, match="destination chain"):
        promote_chain(store_path, "staging", "prod")


def test_promote_missing_key_raises(store_path):
    write_store(store_path, {
        "staging": {"REAL": "val"},
        "prod": {},
    })
    with pytest.raises(PromoteError, match="not found in"):
        promote_chain(store_path, "staging", "prod", keys=["MISSING"])
