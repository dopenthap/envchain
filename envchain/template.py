"""Template rendering for chains — substitute env vars into a string template."""

import re
from envchain.storage import load_store, get_chain


class TemplateError(Exception):
    pass


def render_template(template: str, chain: str, store_path) -> str:
    """Replace {{KEY}} placeholders with values from the given chain."""
    data = load_store(store_path)
    try:
        chain_data = get_chain(data, chain)
    except KeyError:
        raise TemplateError(f"chain '{chain}' not found")

    missing = []

    def replacer(match):
        key = match.group(1).strip()
        if key not in chain_data:
            missing.append(key)
            return match.group(0)
        return chain_data[key]

    result = re.sub(r"\{\{\s*([^}]+?)\s*\}\}", replacer, template)

    if missing:
        raise TemplateError(f"missing keys in chain '{chain}': {', '.join(sorted(missing))}")

    return result


def render_file(template_path: str, chain: str, store_path) -> str:
    """Read a template file and render it against the given chain."""
    try:
        with open(template_path, "r") as f:
            template = f.read()
    except OSError as e:
        raise TemplateError(f"cannot read template file: {e}")
    return render_template(template, chain, store_path)
