"""CLI commands for merging chains."""

import click
from envchain.merge import merge_chains, ChainNotFoundError


@click.command("merge")
@click.argument("src")
@click.argument("dst")
@click.argument("project")
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Let source keys overwrite destination keys on conflict.",
)
def merge_cmd(src, dst, project, overwrite):
    """Merge SRC chain into DST chain for PROJECT.

    By default destination keys win on conflict. Use --overwrite to
    let source keys take precedence.
    """
    try:
        merged = merge_chains(src, dst, project, overwrite=overwrite)
    except ChainNotFoundError as exc:
        raise click.ClickException(str(exc))

    click.echo(f"Merged '{src}' into '{dst}' ({len(merged)} keys total).")
    for key in sorted(merged):
        click.echo(f"  {key}={merged[key]}")
