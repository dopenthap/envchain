"""Archive and restore chains to/from a portable JSON file."""

import json
from pathlib import Path
from typing import Optional

from envchain.storage import load_store, save_store


class ArchiveError(Exception):
    pass


def export_archive(chain_names: list[str], store_path: Path) -> dict:
    """Build an archive dict from the given chain names."""
    store = load_store(store_path)
    archive: dict = {"version": 1, "chains": {}}
    for name in chain_names:
        if name not in store:
            raise ArchiveError(f"Chain not found: {name!r}")
        archive["chains"][name] = store[name]
    return archive


def write_archive(chain_names: list[str], dest: Path, store_path: Path) -> None:
    """Serialize selected chains to a JSON archive file."""
    archive = export_archive(chain_names, store_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(archive, indent=2))


def read_archive(src: Path) -> dict:
    """Load and validate an archive file."""
    if not src.exists():
        raise ArchiveError(f"Archive file not found: {src}")
    try:
        data = json.loads(src.read_text())
    except json.JSONDecodeError as exc:
        raise ArchiveError(f"Invalid archive file: {exc}") from exc
    if data.get("version") != 1 or "chains" not in data:
        raise ArchiveError("Unsupported or malformed archive format")
    return data


def import_archive(
    src: Path,
    store_path: Path,
    overwrite: bool = False,
    only: Optional[list[str]] = None,
) -> list[str]:
    """Import chains from an archive file into the store.

    Returns list of chain names that were imported.
    """
    data = read_archive(src)
    store = load_store(store_path)
    imported = []
    for name, vars_ in data["chains"].items():
        if only and name not in only:
            continue
        if name in store and not overwrite:
            raise ArchiveError(
                f"Chain {name!r} already exists. Use overwrite=True to replace it."
            )
        store[name] = vars_
        imported.append(name)
    save_store(store_path, store)
    return imported
