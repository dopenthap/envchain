"""CLI commands for chain priority management."""

import click
from envchain.storage import get_store_path
from envchain.priority import (
    set_priority,
    get_priority,
    remove_priority,
    list_by_priority,
    PriorityError,
)


@click.group("priority")
def priority_cmd():
    """Manage chain load priority."""


@priority_cmd.command("set")
@click.argument("chain")
@click.argument("priority", type=int)
def set_cmd(chain, priority):
    """Set priority for a chain (lower number = higher priority)."""
    path = get_store_path()
    try:
        set_priority(path, chain, priority)
        click.echo(f"Priority for '{chain}' set to {priority}.")
    except PriorityError as e:
        raise click.ClickException(str(e))


@priority_cmd.command("get")
@click.argument("chain")
def get_cmd(chain):
    """Show priority for a chain."""
    path = get_store_path()
    try:
        val = get_priority(path, chain)
        if val is None:
            click.echo(f"'{chain}' has no priority set.")
        else:
            click.echo(str(val))
    except PriorityError as e:
        raise click.ClickException(str(e))


@priority_cmd.command("remove")
@click.argument("chain")
def remove_cmd(chain):
    """Remove priority from a chain."""
    path = get_store_path()
    try:
        remove_priority(path, chain)
        click.echo(f"Priority removed from '{chain}'.")
    except PriorityError as e:
        raise click.ClickException(str(e))


@priority_cmd.command("list")
def list_cmd():
    """List all chains sorted by priority."""
    path = get_store_path()
    rows = list_by_priority(path)
    if not rows:
        click.echo("No chains found.")
        return
    for name, prio in rows:
        label = str(prio) if prio is not None else "-"
        click.echo(f"{label:>6}  {name}")
