"""CLI commands for chain tier management."""

import click
from envchain.tier import set_tier, get_tier, clear_tier, list_tiers, TierError, VALID_TIERS
from envchain.storage import get_store_path


@click.group("tier")
def tier_cmd():
    """Manage chain tiers (free, dev, staging, prod)."""


@tier_cmd.command("set")
@click.argument("chain")
@click.argument("tier", type=click.Choice(sorted(VALID_TIERS), case_sensitive=False))
def set_cmd(chain, tier):
    """Assign TIER to CHAIN."""
    try:
        set_tier(get_store_path(), chain, tier)
        click.echo(f"Tier for {chain!r} set to {tier.lower()!r}.")
    except TierError as e:
        raise click.ClickException(str(e))


@tier_cmd.command("get")
@click.argument("chain")
def get_cmd(chain):
    """Show the tier for CHAIN."""
    try:
        tier = get_tier(get_store_path(), chain)
        if tier is None:
            click.echo(f"No tier set for {chain!r}.")
        else:
            click.echo(tier)
    except TierError as e:
        raise click.ClickException(str(e))


@tier_cmd.command("clear")
@click.argument("chain")
def clear_cmd(chain):
    """Remove the tier from CHAIN."""
    try:
        clear_tier(get_store_path(), chain)
        click.echo(f"Tier cleared for {chain!r}.")
    except TierError as e:
        raise click.ClickException(str(e))


@tier_cmd.command("list")
def list_cmd():
    """List all chains with a tier assigned."""
    tiers = list_tiers(get_store_path())
    if not tiers:
        click.echo("No tiers set.")
        return
    for chain, tier in sorted(tiers.items()):
        click.echo(f"{chain}: {tier}")
