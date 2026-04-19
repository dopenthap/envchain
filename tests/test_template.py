import pytest
from pathlib import Path
from envchain.template import render_template, render_file, TemplateError
from envchain.storage import save_store


@pytest.fixture
def store_path(tmp_path):
    p = tmp_path / "store.json"
    save_store(p, {
        "mychain": {
            "HOST": "localhost",
            "PORT": "5432",
            "USER": "admin",
        }
    })
    return p


def test_simple_substitution(store_path):
    result = render_template("connect to {{HOST}}:{{PORT}}", "mychain", store_path)
    assert result == "connect to localhost:5432"


def test_whitespace_in_placeholder(store_path):
    result = render_template("user={{ USER }}", "mychain", store_path)
    assert result == "user=admin"


def test_no_placeholders(store_path):
    result = render_template("no vars here", "mychain", store_path)
    assert result == "no vars here"


def test_missing_key_raises(store_path):
    with pytest.raises(TemplateError, match="missing keys"):
        render_template("{{HOST}} {{MISSING}}", "mychain", store_path)


def test_missing_chain_raises(store_path):
    with pytest.raises(TemplateError, match="chain 'nope' not found"):
        render_template("{{HOST}}", "nope", store_path)


def test_render_file(store_path, tmp_path):
    tpl = tmp_path / "config.tpl"
    tpl.write_text("host={{HOST}}\nport={{PORT}}\n")
    result = render_file(str(tpl), "mychain", store_path)
    assert result == "host=localhost\nport=5432\n"


def test_render_file_missing_file(store_path):
    with pytest.raises(TemplateError, match="cannot read template file"):
        render_file("/nonexistent/file.tpl", "mychain", store_path)
