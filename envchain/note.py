"""Per-chain freeform notes (multi-line text attached to a chain)."""

from __future__ import annotations

from envchain.storage import load_store, save_store


class NoteError(Exception):
    pass


def _note_key(chain: str) -> str:
    return f"__note__{chain}"


def set_note(chain: str, text: str, store_path=None) -> None:
    """Attach a freeform note to *chain*, replacing any existing note."""
    store = load_store(store_path)
    if chain not in store:
        raise NoteError(f"chain '{chain}' not found")
    store[_note_key(chain)] = text
    save_store(store, store_path)


def get_note(chain: str, store_path=None) -> str | None:
    """Return the note for *chain*, or None if none has been set."""
    store = load_store(store_path)
    if chain not in store:
        raise NoteError(f"chain '{chain}' not found")
    return store.get(_note_key(chain))


def clear_note(chain: str, store_path=None) -> None:
    """Remove the note for *chain* (no-op if none exists)."""
    store = load_store(store_path)
    if chain not in store:
        raise NoteError(f"chain '{chain}' not found")
    store.pop(_note_key(chain), None)
    save_store(store, store_path)


def list_notes(store_path=None) -> dict[str, str]:
    """Return a mapping of chain name -> note for all chains that have a note."""
    store = load_store(store_path)
    prefix = "__note__"
    return {
        key[len(prefix):]: value
        for key, value in store.items()
        if key.startswith(prefix)
    }
