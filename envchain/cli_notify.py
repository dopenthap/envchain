"""CLI commands for managing chain notification hooks."""

import click

from envchain.notify import NotifyError, get_notify, list_notify, remove_notify, set_notify
from envchain.storage import get_store_path, load_store, save_store


@click.group("notify")
def notify_cmd():
    """Manage activation/deactivation hooks for chains."""


@notify_cmd.command("set")
@click.argument("chain")
@click.argument("event", type=click.Choice(["activate", "deactivate"]))
@click.argument("command")
def set_cmd(chain: str, event: str, command: str) -> None:
    """Set a shell COMMAND to run on EVENT for CHAIN."""
    path = get_store_path()
    store = load_store(path)
    try:
        set_notify(store, chain, event, command)
    except NotifyError as exc:
        raise click.ClickException(str(exc))
    save_store(path, store)
    click.echo(f"Hook set: {chain} [{event}] -> {command}")


@notify_cmd.command("remove")
@click.argument("chain")
@click.argument("event", type=click.Choice(["activate", "deactivate"]))
def remove_cmd(chain: str, event: str) -> None:
    """Remove the EVENT hook from CHAIN."""
    path = get_store_path()
    store = load_store(path)
    try:
        remove_notify(store, chain, event)
    except NotifyError as exc:
        raise click.ClickException(str(exc))
    save_store(path, store)
    click.echo(f"Hook removed: {chain} [{event}]")


@notify_cmd.command("show")
@click.argument("chain")
@click.argument("event", type=click.Choice(["activate", "deactivate"]), required=False)
def show_cmd(chain: str, event: str | None) -> None:
    """Show hook(s) for CHAIN. Optionally filter by EVENT."""
    path = get_store_path()
    store = load_store(path)
    if event:
        cmd = get_notify(store, chain, event)
        if cmd is None:
            click.echo(f"No '{event}' hook for chain '{chain}'.")
        else:
            click.echo(cmd)
    else:
        hooks = list_notify(store, chain)
        if not hooks:
            click.echo(f"No hooks set for chain '{chain}'.")
        else:
            for ev in sorted(hooks):
                click.echo(f"{ev}: {hooks[ev]}")
