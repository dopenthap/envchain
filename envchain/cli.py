import sys
import click
from envchain.storage import get_chain, set_chain, list_chains, delete_chain


@click.group()
def cli():
    """envchain — manage named environment variable sets per project."""
    pass


@cli.command("set")
@click.argument("chain")
@click.argument("key")
@click.argument("value")
def set_var(chain, key, value):
    """Set a variable in a chain."""
    env = get_chain(chain) or {}
    env[key] = value
    set_chain(chain, env)
    click.echo(f"Set {key} in chain '{chain}'.")


@cli.command("get")
@click.argument("chain")
@click.argument("key", required=False)
def get_var(chain, key):
    """Get variables from a chain."""
    env = get_chain(chain)
    if env is None:
        click.echo(f"Chain '{chain}' not found.", err=True)
        sys.exit(1)
    if key:
        if key not in env:
            click.echo(f"Key '{key}' not found in chain '{chain}'.", err=True)
            sys.exit(1)
        click.echo(env[key])
    else:
        for k, v in env.items():
            click.echo(f"{k}={v}")


@cli.command("list")
def list_cmd():
    """List all chains."""
    chains = list_chains()
    if not chains:
        click.echo("No chains defined.")
    else:
        for name in chains:
            click.echo(name)


@cli.command("delete")
@click.argument("chain")
@click.option("--yes", is_flag=True, help="Skip confirmation.")
def delete_cmd(chain, yes):
    """Delete a chain."""
    if not yes:
        click.confirm(f"Delete chain '{chain}'?", abort=True)
    if delete_chain(chain):
        click.echo(f"Chain '{chain}' deleted.")
    else:
        click.echo(f"Chain '{chain}' not found.", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
