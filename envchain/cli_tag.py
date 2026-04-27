"""CLI commands for tagging chains."""

import click
from envchain.storage import get_store_path
from envchain.tag import add_tag, remove_tag, get_tags, find_by_tag, TagError


@click.group("tag")
def tag_cmd():
    """Tag chains for easier organization."""
    pass


@tag_cmd.command("add")
@click.argument("chain")
@click.argument("tag")
def add_cmd(chain, tag):
    """Add a tag to a chain."""
    try:
        add_tag(get_store_path(), chain, tag)
        click.echo(f"Tagged '{chain}' with '{tag}'")
    except TagError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@tag_cmd.command("remove")
@click.argument("chain")
@click.argument("tag")
def remove_cmd(chain, tag):
    """Remove a tag from a chain."""
    try:
        remove_tag(get_store_path(), chain, tag)
        click.echo(f"Removed tag '{tag}' from '{chain}'")
    except TagError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@tag_cmd.command("list")
@click.argument("chain")
def list_cmd(chain):
    """List tags for a chain."""
    try:
        tags = get_tags(get_store_path(), chain)
    except TagError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if tags:
        for t in tags:
            click.echo(t)
    else:
        click.echo(f"No tags for '{chain}'")


@tag_cmd.command("find")
@click.argument("tag")
def find_cmd(tag):
    """Find chains with a given tag."""
    chains = find_by_tag(get_store_path(), tag)
    if chains:
        for c in chains:
            click.echo(c)
    else:
        click.echo(f"No chains tagged '{tag}'")
