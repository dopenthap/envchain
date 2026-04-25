"""CLI commands for managing per-chain key quotas."""

import click
from envchain.quota import (
    QuotaError,
    set_quota,
    remove_quota,
    get_quota,
    check_quota,
    list_quotas,
)
from envchain.storage import get_store_path


@click.group(name="quota")
def quota_cmd():
    """Manage key count quotas for chains."""


@quota_cmd.command(name="set")
@click.argument("chain")
@click.argument("limit", type=int)
@click.option("--store", default=None, help="Path to store file.")
def set_cmd(chain, limit, store):
    """Set the maximum number of keys allowed in CHAIN."""
    store_path = get_store_path(store)
    try:
        set_quota(store_path, chain, limit)
        click.echo(f"Quota for '{chain}' set to {limit} key(s).")
    except QuotaError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@quota_cmd.command(name="remove")
@click.argument("chain")
@click.option("--store", default=None, help="Path to store file.")
def remove_cmd(chain, store):
    """Remove the quota limit for CHAIN."""
    store_path = get_store_path(store)
    try:
        remove_quota(store_path, chain)
        click.echo(f"Quota removed for '{chain}'.")
    except QuotaError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@quota_cmd.command(name="show")
@click.argument("chain")
@click.option("--store", default=None, help="Path to store file.")
def show_cmd(chain, store):
    """Show the quota and current key count for CHAIN."""
    store_path = get_store_path(store)
    try:
        limit = get_quota(store_path, chain)
        usage = check_quota(store_path, chain)
        if limit is None:
            click.echo(f"Chain '{chain}': no quota set (current keys: {usage['count']})")
        else:
            status = "OK" if usage["count"] <= limit else "EXCEEDED"
            click.echo(
                f"Chain '{chain}': {usage['count']}/{limit} keys [{status}]"
            )
    except QuotaError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@quota_cmd.command(name="list")
@click.option("--store", default=None, help="Path to store file.")
def list_cmd(store):
    """List all chains that have quotas set."""
    store_path = get_store_path(store)
    quotas = list_quotas(store_path)
    if not quotas:
        click.echo("No quotas configured.")
        return
    for chain, limit in sorted(quotas.items()):
        click.echo(f"{chain}: {limit}")
