"""CLI commands for chain ownership."""

from __future__ import annotations

import click

from envchain.owner import OwnerError, set_owner, get_owner, clear_owner, list_owners
from envchain.storage import get_store_path


@click.group("owner")
def owner_cmd():
    """Manage chain ownership."""


@owner_cmd.command("set")
@click.argument("chain")
@click.argument("owner")
def set_cmd(chain: str, owner: str) -> None:
    """Assign OWNER to CHAIN."""
    try:
        set_owner(chain, owner, store_path=get_store_path())
        click.echo(f"Owner of '{chain}' set to '{owner}'.")
    except OwnerError as exc:
        raise click.ClickException(str(exc)) from exc


@owner_cmd.command("get")
@click.argument("chain")
def get_cmd(chain: str) -> None:
    """Show the owner of CHAIN."""
    try:
        owner = get_owner(chain, store_path=get_store_path())
    except OwnerError as exc:
        raise click.ClickException(str(exc)) from exc
    if owner is None:
        click.echo(f"No owner set for '{chain}'.")
    else:
        click.echo(owner)


@owner_cmd.command("clear")
@click.argument("chain")
def clear_cmd(chain: str) -> None:
    """Remove the owner entry from CHAIN."""
    try:
        clear_owner(chain, store_path=get_store_path())
        click.echo(f"Owner cleared for '{chain}'.")
    except OwnerError as exc:
        raise click.ClickException(str(exc)) from exc


@owner_cmd.command("list")
def list_cmd() -> None:
    """List all chains with an assigned owner."""
    owners = list_owners(store_path=get_store_path())
    if not owners:
        click.echo("No owners assigned.")
        return
    for chain, owner in sorted(owners.items()):
        click.echo(f"{chain}\t{owner}")
