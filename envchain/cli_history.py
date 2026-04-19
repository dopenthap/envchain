"""CLI commands for activation history."""

import click
from envchain.history import record_activation, get_last_chain, list_history


@click.group("history")
def history_cmd():
    """View or manage chain activation history."""


@history_cmd.command("record")
@click.argument("project")
@click.argument("chain")
def record_cmd(project, chain):
    """Record that CHAIN was activated for PROJECT."""
    record_activation(project, chain)
    click.echo(f"Recorded: {project} -> {chain}")


@history_cmd.command("last")
@click.argument("project")
def last_cmd(project):
    """Show the last activated chain for PROJECT."""
    chain = get_last_chain(project)
    if chain is None:
        click.echo(f"No history for project '{project}'.", err=True)
        raise SystemExit(1)
    click.echo(chain)


@history_cmd.command("list")
def list_cmd():
    """List all recorded project -> chain mappings."""
    data = list_history()
    if not data:
        click.echo("No history recorded.")
        return sorted(data.items()):
        click.echo(f"{project}: {chain}")
