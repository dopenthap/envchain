import click
from envchain.storage import get_store_path
from envchain.badge import BadgeError, set_badge, get_badge, clear_badge, list_badges


@click.group("badge")
def badge_cmd():
    """Manage display badges for chains."""


@badge_cmd.command("set")
@click.argument("chain")
@click.argument("badge")
def set_cmd(chain, badge):
    """Attach BADGE text to CHAIN."""
    store_path = get_store_path()
    try:
        set_badge(store_path, chain, badge)
        click.echo(f"Badge set for '{chain}': {badge.strip()}")
    except BadgeError as e:
        raise click.ClickException(str(e))


@badge_cmd.command("get")
@click.argument("chain")
def get_cmd(chain):
    """Show the badge for CHAIN."""
    store_path = get_store_path()
    try:
        value = get_badge(store_path, chain)
        if value is None:
            click.echo(f"No badge set for '{chain}'.")
        else:
            click.echo(value)
    except BadgeError as e:
        raise click.ClickException(str(e))


@badge_cmd.command("clear")
@click.argument("chain")
def clear_cmd(chain):
    """Remove the badge from CHAIN."""
    store_path = get_store_path()
    try:
        clear_badge(store_path, chain)
        click.echo(f"Badge cleared for '{chain}'.")
    except BadgeError as e:
        raise click.ClickException(str(e))


@badge_cmd.command("list")
def list_cmd():
    """List all chains that have a badge."""
    store_path = get_store_path()
    badges = list_badges(store_path)
    if not badges:
        click.echo("No badges set.")
        return
    for chain, badge in sorted(badges.items()):
        click.echo(f"{chain}: {badge}")
