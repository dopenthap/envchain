"""CLI commands for chain region management."""

import click

from envchain.region import RegionError, clear_region, get_region, list_by_region, set_region
from envchain.storage import get_store_path


@click.group("region")
def region_cmd():
    """Assign and query deployment regions for chains."""


@region_cmd.command("set")
@click.argument("chain")
@click.argument("region")
def set_cmd(chain, region):
    """Assign REGION to CHAIN."""
    try:
        set_region(get_store_path(), chain, region)
        click.echo(f"Region '{region}' set for chain '{chain}'.")
    except RegionError as exc:
        raise click.ClickException(str(exc))


@region_cmd.command("get")
@click.argument("chain")
def get_cmd(chain):
    """Show the region assigned to CHAIN."""
    try:
        region = get_region(get_store_path(), chain)
    except RegionError as exc:
        raise click.ClickException(str(exc))
    if region is None:
        click.echo(f"No region set for chain '{chain}'.")
    else:
        click.echo(region)


@region_cmd.command("clear")
@click.argument("chain")
def clear_cmd(chain):
    """Remove the region assignment from CHAIN."""
    try:
        clear_region(get_store_path(), chain)
        click.echo(f"Region cleared for chain '{chain}'.")
    except RegionError as exc:
        raise click.ClickException(str(exc))


@region_cmd.command("list")
@click.argument("region")
def list_cmd(region):
    """List all chains assigned to REGION."""
    try:
        chains = list_by_region(get_store_path(), region)
    except RegionError as exc:
        raise click.ClickException(str(exc))
    if not chains:
        click.echo(f"No chains in region '{region}'.")
    else:
        for name in chains:
            click.echo(name)
