"""Color/theme support for chain output display."""

from __future__ import annotations

VALID_COLORS = {"red", "green", "blue", "yellow", "cyan", "magenta", "white", "none"}


class ColorError(Exception):
    pass


def _color_key(chain: str) -> str:
    return f"__color__{chain}"


def set_color(store: dict, chain: str, color: str) -> None:
    """Assign a display color to a chain."""
    if chain not in store:
        raise ColorError(f"chain not found: {chain}")
    color = color.strip().lower()
    if color not in VALID_COLORS:
        raise ColorError(
            f"invalid color '{color}'; choose from: {', '.join(sorted(VALID_COLORS))}"
        )
    store[_color_key(chain)] = color


def get_color(store: dict, chain: str) -> str | None:
    """Return the display color for a chain, or None if not set."""
    if chain not in store:
        raise ColorError(f"chain not found: {chain}")
    return store.get(_color_key(chain))


def clear_color(store: dict, chain: str) -> None:
    """Remove the display color for a chain."""
    if chain not in store:
        raise ColorError(f"chain not found: {chain}")
    key = _color_key(chain)
    if key not in store:
        raise ColorError(f"no color set for chain: {chain}")
    del store[key]


def list_colors(store: dict) -> dict[str, str]:
    """Return a mapping of chain name -> color for all chains that have a color set."""
    prefix = "__color__"
    return {
        k[len(prefix):]: v
        for k, v in store.items()
        if k.startswith(prefix)
    }
