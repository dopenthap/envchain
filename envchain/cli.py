import click
from envchain.storage import get_chain, set_chain, delete_chain, list_chains
from envchain.export import export_chain, SUPPORTED_FORMATS


@click.group()
def cli():
    """envchain — manage named environment variable sets."""
    pass


@cli.command("set")
@click.argument("chain")
@click.argument("key")
@click.argument("value")
def set_var(chain, key, value):
    """Set a variable in a chain."""
    set_chain(chain, key, value)
    click.echo(f"Set {key} in chain '{chain}'")


@cli.command("get")
@click.argument("chain")
@click.argument("key", required=False)
def get_var(chain, key):
    """Get a variable (or all) from a chain."""
    vars = get_chain(chain)
    if not vars:
        click.echo(f"Chain '{chain}' is empty or does not exist.", err=True)
        return
    if key:
        val = vars.get(key)
        if val is None:
            click.echo(f"Key '{key}' not found in chain '{chain}'.", err=True)
        else:
            click.echo(val)
    else:
        for k, v in sorted(vars.items()):
            click.echo(f"{k}={v}")


@cli.command("list")
def list_cmd():
    """List all chains."""
    chains = list_chains()
    if not chains:
        click.echo("No chains defined.")
    for name in sorted(chains):
        click.echo(name)


@cli.command("delete")
@click.argument("chain")
@click.argument("key", required=False)
def delete_cmd(chain, key):
    """Delete a chain or a key within a chain."""
    delete_chain(chain, key)
    if key:
        click.echo(f"Deleted key '{key}' from chain '{chain}'")
    else:
        click.echo(f"Deleted chain '{chain}'")


@cli.command("export")
@click.argument("chain")
@click.option("--format", "fmt", default="bash", show_default=True,
              type=click.Choice(SUPPORTED_FORMATS), help="Output format")
@click.option("--prefix", default=None, help="Prefix to prepend to variable names")
def export_cmd(chain, fmt, prefix):
    """Export a chain as shell export statements."""
    vars = get_chain(chain)
    if not vars:
        click.echo(f"Chain '{chain}' is empty or does not exist.", err=True)
        return
    click.echo(export_chain(vars, fmt=fmt, prefix=prefix))
