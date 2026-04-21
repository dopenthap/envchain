"""CLI commands for per-chain notes."""

from __future__ import annotations

import click

from envchain.note import NoteError, clear_note, get_note, list_notes, set_note
from envchain.storage import get_store_path


@click.group("note")
def note_cmd():
    """Manage freeform notes attached to chains."""


@note_cmd.command("set")
@click.argument("chain")
@click.argument("text")
def set_cmd(chain: str, text: str):
    """Attach TEXT as a note on CHAIN."""
    try:
        set_note(chain, text, get_store_path())
        click.echo(f"Note set for '{chain}'.")
    except NoteError as exc:
        raise click.ClickException(str(exc))


@note_cmd.command("get")
@click.argument("chain")
def get_cmd(chain: str):
    """Print the note for CHAIN."""
    try:
        note = get_note(chain, get_store_path())
    except NoteError as exc:
        raise click.ClickException(str(exc))

    if note is None:
        click.echo(f"No note set for '{chain}'.")
    else:
        click.echo(note)


@note_cmd.command("clear")
@click.argument("chain")
def clear_cmd(chain: str):
    """Remove the note from CHAIN."""
    try:
        clear_note(chain, get_store_path())
        click.echo(f"Note cleared for '{chain}'.")
    except NoteError as exc:
        raise click.ClickException(str(exc))


@note_cmd.command("list")
def list_cmd():
    """List all chains that have a note."""
    notes = list_notes(get_store_path())
    if not notes:
        click.echo("No notes found.")
        return
    for chain in sorted(notes):
        preview = notes[chain].splitlines()[0][:60]
        click.echo(f"{chain}: {preview}")
