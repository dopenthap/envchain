"""CLI commands for cloning chains."""

import click

from envchain.clone import CloneError, clone_chain
from envchain.storage import get_store_path


@click.group(name="clone")
def clone_cmd():
    """Clone a chain to a new name."""


@clone_cmd.command(name="create")
@click.argument("src")
@click.argument("dst")
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite destination chain if it already exists.",
)
@click.option(
    "--store",
    default=None,
    envvar="ENVCHAIN_STORE",
    help="Path to the store file.",
)
def create_cmd(src: str, dst: str, overwrite: bool, store: str | None):
    """Clone SRC chain into a new chain named DST.

    All variables from SRC are copied into DST. Metadata such as tags,
    locks, and pins are NOT carried over — DST starts clean.

    Example:

        envchain clone create staging production
    """
    store_path = get_store_path(store)
    try:
        clone_chain(store_path, src, dst, overwrite=overwrite)
        click.echo(f"Cloned '{src}' → '{dst}'.")
    except CloneError as exc:
        raise click.ClickException(str(exc)) from exc


@clone_cmd.command(name="list")
@click.option(
    "--store",
    default=None,
    envvar="ENVCHAIN_STORE",
    help="Path to the store file.",
)
def list_cmd(store: str | None):
    """List all available chains (useful before cloning)."""
    from envchain.storage import load_store

    store_path = get_store_path(store)
    data = load_store(store_path)

    # Filter out internal metadata keys (prefixed with __)
    chains = sorted(k for k in data if not k.startswith("__"))

    if not chains:
        click.echo("No chains found.")
        return

    for name in chains:
        click.echo(name)
