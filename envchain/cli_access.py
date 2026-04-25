"""CLI commands for chain access control."""

import click

from envchain.storage import get_store_path
from envchain.access import AccessError, set_access, remove_access, get_access


@click.group("access")
def access_cmd():
    """Manage per-chain user access restrictions."""


@access_cmd.command("set")
@click.argument("chain")
@click.argument("users", nargs=-1, required=True)
def set_cmd(chain, users):
    """Set allowed users for CHAIN."""
    store_path = get_store_path()
    try:
        set_access(store_path, chain, list(users))
        click.echo(f"Access set for '{chain}': {', '.join(sorted(set(users)))}")
    except AccessError as exc:
        raise click.ClickException(str(exc))


@access_cmd.command("remove")
@click.argument("chain")
def remove_cmd(chain):
    """Remove access restrictions from CHAIN."""
    store_path = get_store_path()
    try:
        remove_access(store_path, chain)
        click.echo(f"Access restrictions removed from '{chain}'.")
    except AccessError as exc:
        raise click.ClickException(str(exc))


@access_cmd.command("show")
@click.argument("chain")
def show_cmd(chain):
    """Show allowed users for CHAIN."""
    store_path = get_store_path()
    allowed = get_access(store_path, chain)
    if allowed is None:
        click.echo(f"'{chain}' is unrestricted (all users allowed).")
    else:
        click.echo(f"Allowed users for '{chain}':")
        for user in allowed:
            click.echo(f"  {user}")
