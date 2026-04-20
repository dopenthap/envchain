"""CLI command for renaming a chain."""

import click
from envchain.rename import rename_chain, RenameError
from envchain.storage import get_store_path


@click.command("rename")
@click.argument("src")
@click.argument("dst")
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite the destination chain if it already exists.",
)
@click.pass_context
def rename_cmd(ctx, src: str, dst: str, overwrite: bool) -> None:
    """Rename chain SRC to DST.

    All variables and associated metadata (tags, lock status, snapshots)
    are transferred to the new name.
    """
    store_path = get_store_path()
    try:
        rename_chain(store_path, src, dst, overwrite=overwrite)
    except RenameError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Renamed '{src}' → '{dst}'.")
