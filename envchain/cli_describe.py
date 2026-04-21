"""CLI commands for managing chain descriptions."""

import click

from envchain.describe import (
    DescribeError,
    clear_description,
    get_description,
    list_descriptions,
    set_description,
)
from envchain.storage import get_store_path, load_store, save_store


@click.group("describe")
def describe_cmd():
    """Manage human-readable descriptions for chains."""


@describe_cmd.command("set")
@click.argument("chain")
@click.argument("text")
@click.option("--store", default=None, help="Path to store file.")
def set_cmd(chain, text, store):
    """Set a description for CHAIN.

    Example:

        envchain describe set myproject "Production environment variables"
    """
    path = get_store_path(store)
    data = load_store(path)
    try:
        set_description(data, chain, text)
        save_store(path, data)
        click.echo(f"Description set for '{chain}'.")
    except DescribeError as exc:
        raise click.ClickException(str(exc)) from exc


@describe_cmd.command("get")
@click.argument("chain")
@click.option("--store", default=None, help="Path to store file.")
def get_cmd(chain, store):
    """Print the description for CHAIN."""
    path = get_store_path(store)
    data = load_store(path)
    try:
        desc = get_description(data, chain)
    except DescribeError as exc:
        raise click.ClickException(str(exc)) from exc

    if desc is None:
        click.echo(f"No description set for '{chain}'.")
    else:
        click.echo(desc)


@describe_cmd.command("clear")
@click.argument("chain")
@click.option("--store", default=None, help="Path to store file.")
def clear_cmd(chain, store):
    """Remove the description for CHAIN."""
    path = get_store_path(store)
    data = load_store(path)
    try:
        clear_description(data, chain)
        save_store(path, data)
        click.echo(f"Description cleared for '{chain}'.")
    except DescribeError as exc:
        raise click.ClickException(str(exc)) from exc


@describe_cmd.command("list")
@click.option("--store", default=None, help="Path to store file.")
def list_cmd(store):
    """List all chains that have descriptions."""
    path = get_store_path(store)
    data = load_store(path)
    entries = list_descriptions(data)

    if not entries:
        click.echo("No descriptions found.")
        return

    max_len = max(len(chain) for chain, _ in entries)
    for chain, desc in sorted(entries):
        click.echo(f"{chain:<{max_len}}  {desc}")
