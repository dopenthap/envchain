"""CLI command for comparing two chains."""

import click
from envchain.compare import compare_chains, CompareError
from envchain.storage import get_store_path


@click.group("compare")
def compare_cmd():
    """Compare two chains side by side."""


@compare_cmd.command("show")
@click.argument("chain_a")
@click.argument("chain_b")
@click.option("--summary", is_flag=True, help="Show only counts, not key names.")
def show_cmd(chain_a, chain_b, summary):
    """Show differences between CHAIN_A and CHAIN_B."""
    store_path = get_store_path()
    try:
        result = compare_chains(store_path, chain_a, chain_b)
    except CompareError as e:
        raise click.ClickException(str(e))

    if summary:
        s = result.summary()
        click.echo(f"only in {chain_a}: {s['only_in_a']}")
        click.echo(f"only in {chain_b}: {s['only_in_b']}")
        click.echo(f"shared same:      {s['shared_same']}")
        click.echo(f"shared different: {s['shared_different']}")
        return

    if not result.has_differences():
        click.echo(f"No differences between '{chain_a}' and '{chain_b}'.")
        return

    if result.only_in_a:
        click.echo(f"Only in {chain_a}:")
        for key in result.only_in_a:
            click.echo(f"  - {key}")

    if result.only_in_b:
        click.echo(f"Only in {chain_b}:")
        for key in result.only_in_b:
            click.echo(f"  + {key}")

    if result.shared_different:
        click.echo("Changed keys:")
        for key in result.shared_different:
            click.echo(f"  ~ {key}")

    if result.shared_same:
        click.echo(f"Shared unchanged: {len(result.shared_same)} key(s)")
