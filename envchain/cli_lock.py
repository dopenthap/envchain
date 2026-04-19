import click
from envchain.storage import get_store_path
from envchain.lock import lock_chain, unlock_chain, list_locked, LockError


@click.group("lock")
def lock_cmd():
    """Lock or unlock chains to prevent modification."""


@lock_cmd.command("add")
@click.argument("chain")
def add_cmd(chain):
    """Lock a chain."""
    store_path = get_store_path()
    try:
        lock_chain(store_path, chain)
        click.echo(f"Locked chain '{chain}'.")
    except LockError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@lock_cmd.command("remove")
@click.argument("chain")
def remove_cmd(chain):
    """Unlock a chain."""
    store_path = get_store_path()
    try:
        unlock_chain(store_path, chain)
        click.echo(f"Unlocked chain '{chain}'.")
    except LockError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@lock_cmd.command("list")
def list_cmd():
    """List all locked chains."""
    store_path = get_store_path()
    locked = list_locked(store_path)
    if not locked:
        click.echo("No locked chains.")
    else:
        for name in locked:
            click.echo(name)
