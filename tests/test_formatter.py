import logging

import pytest

from logfmter.formatter import Logfmter


@pytest.mark.parametrize(
    "value,expected",
    [
        # If the string contains a space, then it must be quoted.
        (" ", '" "'),
        # If the string contains a equals sign, then it must be quoted.
        ("=", '"="'),
        # All double quotes must be escaped.
        ('"', '\\"'),
        # If the string requires escaping and quoting, then both
        # operations should be performed.
        (' "', '" \\""'),
        # If the string is empty, then it should be quoted.
        ("", '""'),
    ],
)
def test_format_string(value, expected):
    assert Logfmter.format_string(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        # None values will be converted to an empty string.
        (None, ""),
        # True values will be converted to "true".
        (True, "true"),
        # False values wll be converted to "false".
        (False, "false"),
        # Numbers will be converted to their string representation.
        (1, "1"),
        # Strings will be passed through the `format_string` function.
        ("=", '"="'),
        # Objects will be converted to their string representation using `str`.
        (Exception("="), '"="'),
    ],
)
def test_format_value(value, expected):
    assert Logfmter.format_value(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [({"a": 1}, "a=1"), ({"a": 1, "b": 2}, "a=1 b=2"), ({"a": " "}, 'a=" "')],
)
def test_format_params(value, expected):
    assert Logfmter.format_params(value) == expected


@pytest.mark.parametrize(
    "record,expected",
    [({"msg": "test"}, {}), ({"value": 1}, {"value": 1})],
)
def test_get_extra(record, expected):
    # Generate a real `logging.LogRecord` from the provided dictionary.
    record = logging.makeLogRecord(record)

    assert Logfmter.get_extra(record) == expected


@pytest.mark.parametrize(
    "record,expected",
    [
        # When providing a dictionary as the log msg, the msg keys
        # will be used as logfmt parameters.
        ({"levelname": "INFO", "msg": {"a": 1}}, "at=INFO a=1"),
        # When providing extra parameters, they will be combined with
        # msg string in the final logfmt parameters.
        ({"levelname": "INFO", "msg": "test", "a": 1}, "at=INFO msg=test a=1"),
        # All parameter values will be passed through the format pipeline.
        ({"levelname": "INFO", "msg": "="}, 'at=INFO msg="="'),
    ],
)
def test_logfmt_formatter_format(record, expected):
    # Generate a real `logging.LogRecord` from the provided dictionary.
    record = logging.makeLogRecord(record)

    assert Logfmter().format(record) == expected
