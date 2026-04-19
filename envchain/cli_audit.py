"""CLI commands for audit log."""

import click
from envchain.audit import load_events, clear_events, get_audit_path
from pathlib import Path


@click.group("audit")
def audit_cmd():
    """View and manage the audit log."""


@audit_cmd.command("log")
@click.option("--chain", default=None, help="Filter by chain name.")
@click.option("--action", default=None, help="Filter by action type.")
@click.option("--limit", default=50, show_default=True, help="Max entries to show.")
def log_cmd(chain, action, limit):
    """Show recent audit log entries."""
    events = load_events()
    if chain:
        events = [e for e in events if e["chain"] == chain]
    if action:
        events = [e for e in events if e["action"] == action]
    events = events[-limit:]
    if not events:
        click.echo("No audit entries found.")
        return
    for e in events:
        detail = f" ({e['detail']}" + ")" if e["detail"] else ""
        click.echo(f"{e['ts']}  {e['action']:<12} {e['chain']}{detail}")


@audit_cmd.command("clear")
@click.confirmation_option(prompt="Clear all audit log entries?")
def clear_cmd():
    """Clear the audit log."""
    clear_events()
    click.echo("Audit log cleared.")


@audit_cmd.command("path")
def path_cmd():
    """Show the path to the audit log file."""
    click.echo(get_audit_path())
