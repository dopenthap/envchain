"""CLI commands for managing chain groups."""

import click
from envchain.storage import get_store_path
from envchain.group import (
    create_group,
    get_group,
    delete_group,
    list_groups,
    add_to_group,
    remove_from_group,
    GroupError,
)


@click.group("group")
def group_cmd():
    """Manage named groups of chains."""


@group_cmd.command("create")
@click.argument("group_name")
@click.argument("chains", nargs=-1, required=True)
def create_cmd(group_name, chains):
    """Create a group containing the specified chains."""
    try:
        create_group(get_store_path(), group_name, list(chains))
        click.echo(f"Group '{group_name}' created with {len(chains)} chain(s).")
    except GroupError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@group_cmd.command("show")
@click.argument("group_name")
def show_cmd(group_name):
    """Show chains in a group."""
    try:
        members = get_group(get_store_path(), group_name)
        if members:
            for chain in members:
                click.echo(chain)
        else:
            click.echo(f"Group '{group_name}' is empty.")
    except GroupError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@group_cmd.command("delete")
@click.argument("group_name")
def delete_cmd(group_name):
    """Delete a group."""
    try:
        delete_group(get_store_path(), group_name)
        click.echo(f"Group '{group_name}' deleted.")
    except GroupError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@group_cmd.command("list")
def list_cmd():
    """List all groups."""
    groups = list_groups(get_store_path())
    if not groups:
        click.echo("No groups defined.")
        return
    for name, members in sorted(groups.items()):
        click.echo(f"{name}: {', '.join(members) if members else '(empty)'}")


@group_cmd.command("add")
@click.argument("group_name")
@click.argument("chain")
def add_cmd(group_name, chain):
    """Add a chain to an existing group."""
    try:
        add_to_group(get_store_path(), group_name, chain)
        click.echo(f"Added '{chain}' to group '{group_name}'.")
    except GroupError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@group_cmd.command("remove")
@click.argument("group_name")
@click.argument("chain")
def remove_cmd(group_name, chain):
    """Remove a chain from a group."""
    try:
        remove_from_group(get_store_path(), group_name, chain)
        click.echo(f"Removed '{chain}' from group '{group_name}'.")
    except GroupError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
