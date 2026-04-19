import pytest
from envchain.validate import validate_chain_name, validate_key, validate_chain_and_key, ValidationError


def test_valid_chain_name():
    assert validate_chain_name("my-project") == []


def test_valid_chain_name_with_dots():
    assert validate_chain_name("prod.us-east.v2") == []


def test_chain_name_empty():
    errors = validate_chain_name("")
    assert any("empty" in e.message for e in errors)


def test_chain_name_starts_with_digit():
    # digits are allowed as non-first chars, but first char can be digit per regex
    assert validate_chain_name("1abc") == []


def test_chain_name_invalid_chars():
    errors = validate_chain_name("my chain!")
    assert len(errors) == 1
    assert errors[0].field == "chain"


def test_chain_name_too_long():
    errors = validate_chain_name("a" * 129)
    assert any("128" in e.message for e in errors)


def test_chain_name_exactly_128():
    assert validate_chain_name("a" * 128) == []


def test_valid_key():
    assert validate_key("MY_VAR") == []


def test_key_empty():
    errors = validate_key("")
    assert any("empty" in e.message for e in errors)


def test_key_starts_with_digit():
    errors = validate_key("1VAR")
    assert len(errors) == 1
    assert errors[0].field == "key"


def test_key_with_space():
    errors = validate_key("MY VAR")
    assert len(errors) == 1


def test_key_too_long():
    errors = validate_key("A" * 257)
    assert any("256" in e.message for e in errors)


def test_key_exactly_256():
    assert validate_key("A" * 256) == []


def test_validate_chain_and_key_both_valid():
    assert validate_chain_and_key("myproject", "API_KEY") == []


def test_validate_chain_and_key_both_invalid():
    errors = validate_chain_and_key("", "")
    fields = [e.field for e in errors]
    assert "chain" in fields
    assert "key" in fields


def test_validation_error_eq():
    a = ValidationError("key", "some message")
    b = ValidationError("key", "some message")
    assert a == b
