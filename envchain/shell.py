"""Shell integration helpers for envchain.

Provides functions to apply a chain's variables to the current shell
by generating eval-able shell snippets or subprocess environments.
"""

import os
from typing import Optional

from envchain.storage import get_chain, ChainNotFoundError


def build_env(chain: str, store_path: Optional[str] = None, base_env: Optional[dict] = None) -> dict:
    """Return a copy of the environment with the chain's variables applied.

    Args:
        chain: Name of the chain to apply.
        store_path: Optional path to the store file.
        base_env: Base environment dict. Defaults to os.environ.

    Returns:
        A new dict with chain variables merged on top of base_env.

    Raises:
        ChainNotFoundError: If the chain does not exist in the store.
    """
    if base_env is None:
        base_env = dict(os.environ)

    vars_ = get_chain(chain, store_path=store_path)
    if vars_ is None:
        raise ChainNotFoundError(f"Chain '{chain}' not found.")

    merged = {**base_env, **vars_}
    return merged


def eval_snippet(chain: str, shell: str = "bash", store_path: Optional[str] = None) -> str:
    """Generate a shell snippet that exports all variables in a chain.

    Intended for use with `eval $(envchain shell <chain>)`.

    Args:
        chain: Name of the chain.
        shell: Target shell — 'bash', 'zsh', or 'fish'.
        store_path: Optional path to the store file.

    Returns:
        A string containing export statements for the given shell.

    Raises:
        ChainNotFoundError: If the chain does not exist.
        ValueError: If the shell is not supported.
    """
    vars_ = get_chain(chain, store_path=store_path)
    if vars_ is None:
        raise ChainNotFoundError(f"Chain '{chain}' not found.")

    supported = {"bash", "zsh", "fish"}
    if shell not in supported:
        raise ValueError(f"Unsupported shell '{shell}'. Choose from: {', '.join(sorted(supported))}")

    lines = []
    for key, value in sorted(vars_.items()):
        escaped = _escape(value)
        if shell == "fish":
            lines.append(f"set -x {key} {escaped};")
        else:
            lines.append(f"export {key}={escaped}")

    return "\n".join(lines)


def _escape(value: str) -> str:
    """Wrap a value in single quotes, escaping any single quotes within."""
    return "'" + value.replace("'", "'\"'\"'") + "'"
