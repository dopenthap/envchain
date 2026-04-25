"""CLI commands for managing chain hooks."""

import click

from envchain.hook import set_hook, remove_hook, get_hook, list_hooks, HookError, HOOK_EVENTS


@click.group("hook")
def hook_cmd():
    """Manage pre/post activation hooks for chains."""


@hook_cmd.command("set")
@click.argument("chain")
@click.argument("event", type=click.Choice(HOOK_EVENTS))
@click.argument("command")
def set_cmd(chain, event, command):
    """Set a hook command for a chain event."""
    try:
        set_hook(chain, event, command)
        click.echo(f"Hook set for '{chain}' on '{event}'.")
    except HookError as e:
        raise click.ClickException(str(e))


@hook_cmd.command("remove")
@click.argument("chain")
@click.argument("event", type=click.Choice(HOOK_EVENTS))
def remove_cmd(chain, event):
    """Remove a hook from a chain event."""
    try:
        remove_hook(chain, event)
        click.echo(f"Hook removed for '{chain}' on '{event}'.")
    except HookError as e:
        raise click.ClickException(str(e))


@hook_cmd.command("show")
@click.argument("chain")
@click.argument("event", type=click.Choice(HOOK_EVENTS))
def show_cmd(chain, event):
    """Show the hook command for a specific event."""
    try:
        cmd = get_hook(chain, event)
        if cmd is None:
            click.echo(f"No hook set for '{chain}' on '{event}'.")
        else:
            click.echo(cmd)
    except HookError as e:
        raise click.ClickException(str(e))


@hook_cmd.command("list")
@click.argument("chain")
def list_cmd(chain):
    """List all hooks for a chain."""
    try:
        hooks = list_hooks(chain)
        if not hooks:
            click.echo(f"No hooks set for '{chain}'.")
            return
        for event, command in sorted(hooks.items()):
            click.echo(f"{event}: {command}")
    except HookError as e:
        raise click.ClickException(str(e))
