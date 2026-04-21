"""CLI commands for label management."""

import click
from envchain.storage import get_store_path
from envchain.label import LabelError, set_label, get_label, clear_label, list_labels


@click.group("label")
def label_cmd():
    """Manage human-friendly labels for chains."""


@label_cmd.command("set")
@click.argument("chain")
@click.argument("label")
def set_cmd(chain, label):
    """Set a display label for CHAIN."""
    store_path = get_store_path()
    try:
        set_label(store_path, chain, label)
        click.echo(f"Label for '{chain}' set to: {label.strip()}")
    except LabelError as e:
        raise click.ClickException(str(e))


@label_cmd.command("get")
@click.argument("chain")
def get_cmd(chain):
    """Get the display label for CHAIN."""
    store_path = get_store_path()
    try:
        label = get_label(store_path, chain)
        if label is None:
            click.echo(f"No label set for '{chain}'.")
        else:
            click.echo(label)
    except LabelError as e:
        raise click.ClickException(str(e))


@label_cmd.command("clear")
@click.argument("chain")
def clear_cmd(chain):
    """Remove the label from CHAIN."""
    store_path = get_store_path()
    try:
        clear_label(store_path, chain)
        click.echo(f"Label cleared for '{chain}'.")
    except LabelError as e:
        raise click.ClickException(str(e))


@label_cmd.command("list")
def list_cmd():
    """List all chains that have labels."""
    store_path = get_store_path()
    labels = list_labels(store_path)
    if not labels:
        click.echo("No labels set.")
        return
    for chain, label in sorted(labels.items()):
        click.echo(f"{chain}: {label}")
