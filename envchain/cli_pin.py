"""CLI commands for pinning chains to snapshot labels."""

import click
from envchain.storage import get_store_path
from envchain.pin import pin_chain, unpin_chain, get_pin, list_pins, PinError


@click.group("pin")
def pin_cmd():
    """Pin chains to snapshot versions."""


@pin_cmd.command("set")
@click.argument("chain")
@click.argument("label")
def set_cmd(chain, label):
    """Pin CHAIN to snapshot LABEL."""
    path = get_store_path()
    try:
        pin_chain(path, chain, label)
        click.echo(f"Pinned '{chain}' to snapshot '{label}'.")
    except PinError as e:
        raise click.ClickException(str(e))


@pin_cmd.command("remove")
@click.argument("chain")
def remove_cmd(chain):
    """Remove pin from CHAIN."""
    path = get_store_path()
    try:
        unpin_chain(path, chain)
        click.echo(f"Unpinned '{chain}'.")
    except PinError as e:
        raise click.ClickException(str(e))


@pin_cmd.command("show")
@click.argument("chain")
def show_cmd(chain):
    """Show pinned snapshot for CHAIN."""
    path = get_store_path()
    label = get_pin(path, chain)
    if label:
        click.echo(label)
    else:
        click.echo(f"'{chain}' is not pinned.")


@pin_cmd.command("list")
def list_cmd():
    """List all pinned chains."""
    path = get_store_path()
    pins = list_pins(path)
    if not pins:
        click.echo("No pins set.")
    else:
        for chain, label in sorted(pins.items()):
            click.echo(f"{chain}: {label}")
