import click
from envchain.lint import lint_store
from envchain.storage import get_store_path


@click.command("lint")
@click.argument("chains", nargs=-1)
@click.option("--store", default=None, hidden=True)
def lint_cmd(chains, store):
    """Check chains for common issues."""
    store_path = store or get_store_path()
    warnings = lint_store(store_path)

    if chains:
        warnings = [w for w in warnings if w.chain in chains]

    if not warnings:
        click.echo("No issues found.")
        return

    grouped: dict[str, list] = {}
    for w in warnings:
        grouped.setdefault(w.chain, []).append(w)

    for chain in sorted(grouped):
        click.echo(f"[{chain}]")
        for w in grouped[chain]:
            click.echo(f"  {w.key}: {w.message}")

    raise SystemExit(1)
