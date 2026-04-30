import click
from envchain.storage import get_store_path
from envchain.version import VersionError, bump_version, get_version, reset_version, list_versions


@click.group("version", help="Track version numbers for chains.")
def version_cmd():
    pass


@version_cmd.command("bump", help="Bump the version counter for a chain.")
@click.argument("chain")
def bump_cmd(chain):
    store_path = get_store_path()
    try:
        v = bump_version(store_path, chain)
        click.echo(f"version: {v}")
    except VersionError as e:
        click.echo(f"error: {e}", err=True)
        raise SystemExit(1)


@version_cmd.command("get", help="Show the current version number for a chain.")
@click.argument("chain")
def get_cmd(chain):
    store_path = get_store_path()
    try:
        v = get_version(store_path, chain)
        click.echo(str(v))
    except VersionError as e:
        click.echo(f"error: {e}", err=True)
        raise SystemExit(1)


@version_cmd.command("reset", help="Reset the version counter for a chain to 0.")
@click.argument("chain")
def reset_cmd(chain):
    store_path = get_store_path()
    try:
        reset_version(store_path, chain)
        click.echo(f"version reset for '{chain}'")
    except VersionError as e:
        click.echo(f"error: {e}", err=True)
        raise SystemExit(1)


@version_cmd.command("list", help="List version numbers for all chains.")
def list_cmd():
    store_path = get_store_path()
    versions = list_versions(store_path)
    if not versions:
        click.echo("no versioned chains")
        return
    for chain, v in sorted(versions.items()):
        click.echo(f"{chain}\t{v}")
