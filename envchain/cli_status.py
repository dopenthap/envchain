"""CLI command for displaying chain status."""

import click
from envchain.status import get_status, StatusError
from envchain.storage import load_store, get_store_path


@click.group("status")
def status_cmd():
    """Show status and metadata for chains."""


@status_cmd.command("show")
@click.argument("chain")
@click.option("--store", default=None, hidden=True)
def show_cmd(chain, store):
    """Show full status for a chain."""
    path = store or get_store_path()
    try:
        status = get_status(chain, path)
        click.echo(status.summary())
    except StatusError as e:
        click.echo(f"error: {e}", err=True)
        raise SystemExit(1)


@status_cmd.command("list")
@click.option("--store", default=None, hidden=True)
def list_cmd(store):
    """Show a one-line status for every chain."""
    path = store or get_store_path()
    data = load_store(path)
    chains = [k for k in data if not k.startswith("__")]
    if not chains:
        click.echo("no chains found")
        return
    for name in sorted(chains):
        try:
            st = get_status(name, path)
            flags = []
            if st.locked:
                flags.append("L")
            if st.protected:
                flags.append("P")
            if st.frozen:
                flags.append("F")
            if st.expired:
                flags.append("X")
            flag_str = f" [{','.join(flags)}]" if flags else ""
            tags_str = f" tags={','.join(st.tags)}" if st.tags else ""
            click.echo(f"{name}{flag_str}  keys={st.key_count}{tags_str}")
        except StatusError:
            click.echo(f"{name}  (error reading status)")
