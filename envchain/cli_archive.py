"""CLI commands for archiving and restoring chains."""

from pathlib import Path

import click

from envchain.archive import write_archive, import_archive, ArchiveError
from envchain.storage import get_store_path


@click.group("archive")
def archive_cmd():
    """Archive chains to a file or restore them from one."""


@archive_cmd.command("export")
@click.argument("chains", nargs=-1, required=True)
@click.option("-o", "--output", required=True, help="Destination archive file (.json)")
@click.option("--store", default=None, hidden=True)
def export_cmd(chains, output, store):
    """Export one or more chains to an archive file."""
    store_path = Path(store) if store else get_store_path()
    dest = Path(output)
    try:
        write_archive(list(chains), dest, store_path)
        click.echo(f"Exported {len(chains)} chain(s) to {dest}")
    except ArchiveError as exc:
        raise click.ClickException(str(exc))


@archive_cmd.command("import")
@click.argument("file", type=click.Path(exists=True))
@click.option("--overwrite", is_flag=True, default=False, help="Replace existing chains")
@click.option(
    "--only",
    multiple=True,
    metavar="CHAIN",
    help="Import only these chains (repeatable)",
)
@click.option("--store", default=None, hidden=True)
def import_cmd(file, overwrite, only, store):
    """Import chains from an archive file."""
    store_path = Path(store) if store else get_store_path()
    src = Path(file)
    try:
        imported = import_archive(src, store_path, overwrite=overwrite, only=list(only) or None)
        for name in sorted(imported):
            click.echo(f"  imported: {name}")
        click.echo(f"Done. {len(imported)} chain(s) imported.")
    except ArchiveError as exc:
        raise click.ClickException(str(exc))
