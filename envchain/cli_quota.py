"""CLI commands for managing per-chain key quotas."""

import click
from envchain.quota import set_quota, remove_quota, get_quota, list_quotas, QuotaError
from envchain.storage import get_store_path


@click.group("quota")
def quota_cmd():
    """Manage key count quotas for chains."""


@quota_cmd.command("set")
@click.argument("chain")
@click.argument("limit", type=int)
def set_cmd(chain, limit):
    """Set the max number of keys allowed in CHAIN."""
    store_path = get_store_path()
    try:
        set_quota(store_path, chain, limit)
        click.echo(f"Quota for '{chain}' set to {limit} key(s).")
    except QuotaError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@quota_cmd.command("remove")
@click.argument("chain")
def remove_cmd(chain):
    """Remove the quota for CHAIN."""
    store_path = get_store_path()
    try:
        remove_quota(store_path, chain)
        click.echo(f"Quota removed for '{chain}'.")
    except QuotaError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@quota_cmd.command("show")
@click.argument("chain")
def show_cmd(chain):
    """Show the quota for CHAIN."""
    store_path = get_store_path()
    try:
        limit = get_quota(store_path, chain)
        if limit is None:
            click.echo(f"No quota set for '{chain}'.")
        else:
            click.echo(f"{chain}: {limit} key(s) max")
    except QuotaError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@quota_cmd.command("list")
def list_cmd():
    """List all chains with quotas."""
    store_path = get_store_path()
    quotas = list_quotas(store_path)
    if not quotas:
        click.echo("No quotas configured.")
        return
    for chain, limit in sorted(quotas.items()):
        click.echo(f"{chain}: {limit}")
