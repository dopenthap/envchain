"""Import environment variables from dotenv or shell export files into a chain."""

import re
from pathlib import Path
from envchain.storage import load_store, save_store, get_store_path


class ImportError(Exception):
    pass


def _parse_dotenv(text: str) -> dict:
    result = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # strip leading 'export '
        line = re.sub(r"^export\s+", "", line)
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        # strip surrounding quotes
        if len(value) >= 2 and value[0] in ('"', "'") and value[-1] == value[0]:
            value = value[1:-1]
        result[key] = value
    return result


def import_from_text(text: str, chain: str, overwrite: bool = False,
                     store_path: Path | None = None) -> dict:
    """Parse dotenv/export text and merge into chain. Returns final chain vars."""
    if store_path is None:
        store_path = get_store_path()

    parsed = _parse_dotenv(text)
    if not parsed:
        raise ImportError("No valid KEY=VALUE pairs found in input")

    store = load_store(store_path)
    existing = store.get("chains", {}).get(chain, {})

    if overwrite:
        merged = {**existing, **parsed}
    else:
        merged = {**parsed, **existing}

    store.setdefault("chains", {})[chain] = merged
    save_store(store_path, store)
    return merged


def import_from_file(path: Path, chain: str, overwrite: bool = False,
                     store_path: Path | None = None) -> dict:
    """Read a file and import its contents into a chain."""
    try:
        text = path.read_text()
    except FileNotFoundError:
        raise ImportError(f"File not found: {path}")
    return import_from_text(text, chain, overwrite=overwrite, store_path=store_path)
