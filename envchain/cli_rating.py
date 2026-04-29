"""CLI commands for chain ratings."""

import click
from envchain.storage import get_store_path
from envchain.rating import (
    set_rating,
    get_rating,
    clear_rating,
    list_ratings,
    RatingError,
)


@click.group("rating")
def rating_cmd():
    """Manage chain ratings (1-5 stars)."""


@rating_cmd.command("set")
@click.argument("chain")
@click.argument("score", type=int)
def set_cmd(chain, score):
    """Set a rating (1-5) for CHAIN."""
    try:
        set_rating(get_store_path(), chain, score)
        stars = "★" * score + "☆" * (5 - score)
        click.echo(f"Rated '{chain}': {stars} ({score}/5)")
    except RatingError as e:
        raise click.ClickException(str(e))


@rating_cmd.command("get")
@click.argument("chain")
def get_cmd(chain):
    """Show the rating for CHAIN."""
    try:
        rating = get_rating(get_store_path(), chain)
        if rating is None:
            click.echo(f"No rating set for '{chain}'")
        else:
            stars = "★" * rating + "☆" * (5 - rating)
            click.echo(f"{chain}: {stars} ({rating}/5)")
    except RatingError as e:
        raise click.ClickException(str(e))


@rating_cmd.command("clear")
@click.argument("chain")
def clear_cmd(chain):
    """Remove the rating for CHAIN."""
    try:
        clear_rating(get_store_path(), chain)
        click.echo(f"Rating cleared for '{chain}'")
    except RatingError as e:
        raise click.ClickException(str(e))


@rating_cmd.command("list")
def list_cmd():
    """List all rated chains."""
    ratings = list_ratings(get_store_path())
    if not ratings:
        click.echo("No chains have been rated.")
        return
    for chain, score in sorted(ratings.items(), key=lambda x: -x[1]):
        stars = "★" * score + "☆" * (5 - score)
        click.echo(f"{chain}: {stars} ({score}/5)")
