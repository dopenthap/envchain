"""CLI commands for managing chain snapshots."""

import click
from envchain.snapshot import (
    SnapshotError,
    create_snapshot,
    restore_snapshot,
    list_snapshots,
    delete_snapshot,
)
from envchain.storage import get_store_path, load_store


@click.group("snapshot")
def snapshot_cmd():
    """Create and restore chain snapshots."""


@snapshot_cmd.command("create")
@click.argument("chain")
@click.option("--label", default=None, help="Optional label for the snapshot.")
def create_cmd(chain, label):
    """Snapshot the current state of a chain."""
    store_path = get_store_path()
    store = load_store(store_path)
    try:
        key = create_snapshot(store, store_path, chain, label=label)
        click.echo(f"Snapshot saved: {key}")
    except SnapshotError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@snapshot_cmd.command("restore")
@click.argument("chain")
@click.argument("label")
@click.option("--overwrite", is_flag=True, default=False, help="Overwrite existing keys.")
def restore_cmd(chain, label, overwrite):
    """Restore a chain from a snapshot."""
    store_path = get_store_path()
    store = load_store(store_path)
    try:
        restore_snapshot(store, store_path, chain, label, overwrite=overwrite)
        click.echo(f"Restored snapshot '{label}' into chain '{chain}'.")
    except SnapshotError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@snapshot_cmd.command("list")
@click.argument("chain")
def list_cmd(chain):
    """List all snapshots for a chain."""
    store_path = get_store_path()
    store = load_store(store_path)
    snapshots = list_snapshots(store, chain)
    if not snapshots:
        click.echo(f"No snapshots found for chain '{chain}'.")
        return
    for label in snapshots:
        click.echo(label)


@snapshot_cmd.command("delete")
@click.argument("chain")
@click.argument("label")
def delete_cmd(chain, label):
    """Delete a specific snapshot."""
    store_path = get_store_path()
    store = load_store(store_path)
    try:
        delete_snapshot(store, store_path, chain, label)
        click.echo(f"Deleted snapshot '{label}' from chain '{chain}'.")
    except SnapshotError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
