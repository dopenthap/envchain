"""CLI commands for chain protection."""

import click
from envchain.storage import get_store_path
from envchain.protect import (
    protect_chain,
    unprotect_chain,
    list_protected,
    ProtectError,
)


@click.group("protect")
def protect_cmd():
    """Manage chain write-protection."""


@protect_cmd.command("add")
@click.argument("chain")
def add_cmd(chain):
    """Mark CHAIN as protected (read-only)."""
    path = get_store_path()
    try:
        protect_chain(chain, path)
        click.echo(f"chain '{chain}' is now protected")
    except ProtectError as exc:
        raise click.ClickException(str(exc))


@protect_cmd.command("remove")
@click.argument("chain")
def remove_cmd(chain):
    """Remove protection from CHAIN."""
    path = get_store_path()
    try:
        unprotect_chain(chain, path)
        click.echo(f"chain '{chain}' is no longer protected")
    except ProtectError as exc:
        raise click.ClickException(str(exc))


@protect_cmd.command("list")
def list_cmd():
    """List all protected chains."""
    path = get_store_path()
    chains = list_protected(path)
    if not chains:
        click.echo("no protected chains")
    else:
        for chain in chains:
            click.echo(chain)
