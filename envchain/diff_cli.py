import click
from envchain.diff import diff_chains
from envchain.storage import load_store


@click.command("diff")
@click.argument("chain_a")
@click.argument("chain_b")
@click.option("--store", default=None, help="Path to store file")
def diff_cmd(chain_a, chain_b, store):
    """Show differences between two chains."""
    data = load_store(store)

    try:
        result = diff_chains(data, chain_a, chain_b)
    except KeyError as e:
        raise click.ClickException(f"Chain not found: {e}")

    if not any(result.values()):
        click.echo("No differences found.")
        return

    for key in sorted(result["only_in_a"]):
        click.echo(f"< {key}")

    for key in sorted(result["only_in_b"]):
        click.echo(f"> {key}")

    for key in sorted(result["changed"]):
        a_val = result["changed"][key]["a"]
        b_val = result["changed"][key]["b"]
        click.echo(f"~ {key}: {a_val!r} -> {b_val!r}")
