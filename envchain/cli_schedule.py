"""CLI commands for chain schedules."""

import click
from envchain.schedule import (
    set_schedule, remove_schedule, get_schedule, list_schedules, ScheduleError
)


@click.group("schedule")
def schedule_cmd():
    """Manage activation schedule reminders for chains."""


@schedule_cmd.command("set")
@click.argument("chain")
@click.argument("cron")
@click.option("--message", "-m", default="", help="Reminder message")
def set_cmd(chain, cron, message):
    """Set a cron schedule reminder for CHAIN."""
    set_schedule(chain, cron, message)
    click.echo(f"Schedule set for '{chain}': {cron}")
    if message:
        click.echo(f"Message: {message}")


@schedule_cmd.command("remove")
@click.argument("chain")
def remove_cmd(chain):
    """Remove the schedule for CHAIN."""
    try:
        remove_schedule(chain)
        click.echo(f"Schedule removed for '{chain}'")
    except ScheduleError as e:
        raise click.ClickException(str(e))


@schedule_cmd.command("show")
@click.argument("chain")
def show_cmd(chain):
    """Show the schedule for CHAIN."""
    try:
        s = get_schedule(chain)
        click.echo(f"chain:   {chain}")
        click.echo(f"cron:    {s['cron']}")
        if s.get("message"):
            click.echo(f"message: {s['message']}")
    except ScheduleError as e:
        raise click.ClickException(str(e))


@schedule_cmd.command("list")
def list_cmd():
    """List all chain schedules."""
    schedules = list_schedules()
    if not schedules:
        click.echo("No schedules defined.")
        return
    for chain, info in sorted(schedules.items()):
        msg = f"  ({info['message']})" if info.get("message") else ""
        click.echo(f"{chain}: {info['cron']}{msg}")
