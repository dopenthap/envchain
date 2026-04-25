"""CLI commands for TTL management."""

import click

from envchain.storage import get_store_path
from envchain.ttl import TtlError, get_ttl, is_expired, list_ttls, remove_ttl, set_ttl


@click.group("ttl")
def ttl_cmd():
    """Manage time-to-live settings for chains."""


@ttl_cmd.command("set")
@click.argument("chain")
@click.argument("seconds", type=int)
def set_cmd(chain, seconds):
    """Set a TTL of SECONDS for CHAIN."""
    store_path = get_store_path()
    try:
        set_ttl(store_path, chain, seconds)
        click.echo(f"TTL set: '{chain}' expires in {seconds}s")
    except TtlError as e:
        raise click.ClickException(str(e))


@ttl_cmd.command("remove")
@click.argument("chain")
def remove_cmd(chain):
    """Remove the TTL for CHAIN."""
    store_path = get_store_path()
    try:
        remove_ttl(store_path, chain)
        click.echo(f"TTL removed for '{chain}'")
    except TtlError as e:
        raise click.ClickException(str(e))


@ttl_cmd.command("show")
@click.argument("chain")
def show_cmd(chain):
    """Show TTL info for CHAIN."""
    store_path = get_store_path()
    try:
        info = get_ttl(store_path, chain)
        if info is None:
            click.echo(f"No TTL set for '{chain}'")
            return
        expired = is_expired(store_path, chain)
        status = "EXPIRED" if expired else "active"
        click.echo(f"chain:      {chain}")
        click.echo(f"seconds:    {info['seconds']}")
        click.echo(f"expires_at: {info['expires_at']:.2f}")
        click.echo(f"status:     {status}")
    except TtlError as e:
        raise click.ClickException(str(e))


@ttl_cmd.command("list")
def list_cmd():
    """List all chains that have a TTL configured."""
    store_path = get_store_path()
    ttls = list_ttls(store_path)
    if not ttls:
        click.echo("No TTLs configured.")
        return
    for chain in sorted(ttls):
        info = ttls[chain]
        expired = is_expired(store_path, chain)
        flag = " [EXPIRED]" if expired else ""
        click.echo(f"{chain}: {info['seconds']}s{flag}")
