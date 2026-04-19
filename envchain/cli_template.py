"""CLI commands for template rendering."""

import click
from envchain.template import render_template, render_file, TemplateError
from envchain.storage import get_store_path


@click.group("template")
def template_cmd():
    """Render templates using chain variables."""


@template_cmd.command("render")
@click.argument("chain")
@click.argument("template_string")
@click.option("--store", default=None, help="Path to store file.")
def render_cmd(chain, template_string, store):
    """Render a template string with variables from CHAIN.

    Placeholders use {{KEY}} syntax.
    """
    store_path = Path(store) if store else get_store_path()
    try:
        result = render_template(template_string, chain, store_path)
        click.echo(result)
    except TemplateError as e:
        raise click.ClickException(str(e))


@template_cmd.command("file")
@click.argument("chain")
@click.argument("template_file", type=click.Path(exists=True))
@click.option("--store", default=None, help="Path to store file.")
@click.option("--output", "-o", default=None, help="Write output to file instead of stdout.")
def file_cmd(chain, template_file, store, output):
    """Render a template FILE with variables from CHAIN."""
    store_path = Path(store) if store else get_store_path()
    try:
        result = render_file(template_file, chain, store_path)
    except TemplateError as e:
        raise click.ClickException(str(e))

    if output:
        with open(output, "w") as f:
            f.write(result)
        click.echo(f"Written to {output}")
    else:
        click.echo(result, nl=False)


from pathlib import Path
