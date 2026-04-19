"""Export environment chains to various shell formats."""

from typing import Optional


SUPPORTED_FORMATS = ["bash", "fish", "dotenv"]


def export_chain(vars: dict, fmt: str = "bash", prefix: Optional[str] = None) -> str:
    """Render a dict of env vars as shell export statements."""
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format '{fmt}'. Choose from: {', '.join(SUPPORTED_FORMATS)}")

    lines = []
    for key, value in sorted(vars.items()):
        full_key = f"{prefix}_{key}" if prefix else key
        escaped = _escape(value)
        if fmt == "bash":
            lines.append(f'export {full_key}="{escaped}"')
        elif fmt == "fish":
            lines.append(f'set -x {full_key} "{escaped}"')
        elif fmt == "dotenv":
            lines.append(f'{full_key}="{escaped}"')
    return "\n".join(lines)


def _escape(value: str) -> str:
    """Escape double quotes and backslashes in a value."""
    return value.replace("\\", "\\\\").replace('"', '\\"')
