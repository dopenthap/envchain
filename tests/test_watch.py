import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from envchain.watch import _chain_hash, watch_chain, WatchError
from envchain.storage import save_store


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "store.json"


def write_store(store_path, data):
    store_path.parent.mkdir(parents=True, exist_ok=True)
    store_path.write_text(json.dumps(data))


def test_chain_hash_returns_string(store_path):
    write_store(store_path, {"chains": {"mychain": {"KEY": "val"}}})
    h = _chain_hash("mychain", store_path)
    assert isinstance(h, str) and len(h) == 64


def test_chain_hash_changes_on_update(store_path):
    write_store(store_path, {"chains": {"mychain": {"KEY": "val"}}})
    h1 = _chain_hash("mychain", store_path)
    write_store(store_path, {"chains": {"mychain": {"KEY": "changed"}}})
    h2 = _chain_hash("mychain", store_path)
    assert h1 != h2


def test_chain_hash_missing_chain(store_path):
    write_store(store_path, {"chains": {}})
    with pytest.raises(WatchError, match="not found"):
        _chain_hash("ghost", store_path)


def test_watch_runs_command_on_change(store_path):
    write_store(store_path, {"chains": {"mychain": {"KEY": "v1"}}})

    call_count = [0]

    def fake_hash(name, path):
        call_count[0] += 1
        # Return a different hash on second call to simulate change
        return "aaa" if call_count[0] == 1 else "bbb"

    with patch("envchain.watch._chain_hash", side_effect=fake_hash), \
         patch("envchain.watch.build_env", return_value={}), \
         patch("envchain.watch.subprocess.run") as mock_run:
        watch_chain("mychain", ["echo", "hi"], interval=0, store_path=store_path, max_iterations=2)
        mock_run.assert_called_once()


def test_watch_no_command_on_first_detection(store_path):
    write_store(store_path, {"chains": {"mychain": {"KEY": "v1"}}})

    with patch("envchain.watch._chain_hash", return_value="stable"), \
         patch("envchain.watch.subprocess.run") as mock_run:
        watch_chain("mychain", ["echo", "hi"], interval=0, store_path=store_path, max_iterations=1)
        mock_run.assert_not_called()
