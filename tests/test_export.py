import pytest
from envchain.export import export_chain, _escape, SUPPORTED_FORMATS


SAMPLE = {"API_KEY": "abc123", "DEBUG": "true"}


def test_bash_format():
    out = export_chain(SAMPLE, fmt="bash")
    assert 'export API_KEY="abc123"' in out
    assert 'export DEBUG="true"' in out


def test_fish_format():
    out = export_chain(SAMPLE, fmt="fish")
    assert 'set -x API_KEY "abc123"' in out
    assert 'set -x DEBUG "true"' in out


def test_dotenv_format():
    out = export_chain(SAMPLE, fmt="dotenv")
    assert 'API_KEY="abc123"' in out
    assert 'DEBUG="true"' in out


def test_prefix():
    out = export_chain({"TOKEN": "xyz"}, fmt="bash", prefix="MY_APP")
    assert 'export MY_APP_TOKEN="xyz"' in out


def test_unsupported_format():
    with pytest.raises(ValueError, match="Unsupported format"):
        export_chain(SAMPLE, fmt="powershell")


def test_escape_quotes():
    assert _escape('say "hi"') == 'say \\"hi\\"'


def test_escape_backslash():
    assert _escape('C:\\path') == 'C:\\\\path'


def test_empty_vars():
    out = export_chain({}, fmt="bash")
    assert out == ""


def test_sorted_output():
    out = export_chain({"Z_VAR": "1", "A_VAR": "2"}, fmt="dotenv")
    lines = out.splitlines()
    assert lines[0].startswith("A_VAR")
    assert lines[1].startswith("Z_VAR")
