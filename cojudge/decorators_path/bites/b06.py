"""Recreated exercise: count help output without leaking stdout."""

SPEC = {
    "title": "Capture stdout",
    "module": "helplen",
    "contract": "get_len_help_text(builtin) accepts objects that satisfy isinstance(value, "
                "types.BuiltinFunctionType), including bound built-in methods. Reject all other objects with "
                "ValueError. Call help(builtin), capture stdout, and return its character count. Do not leak "
                "output. Restore stdout after success and exceptions, and propagate help exceptions. "
                "Help output depends on the Python version; no fixed length is required.",
    "statement": """Implement `get_len_help_text(builtin)`. Accept only `types.BuiltinFunctionType`
objects, such as `len`, `max`, `pow`, or `[].append`. Raise `ValueError` for other
objects, including classes and ordinary Python functions.

Call `help(builtin)`. Capture its standard output and return the number of
characters. Leave standard output restored after the call, including when
`help` raises an exception. Propagate that exception.

Example: if `help(len)` writes `\"Length help\\n\"`, return `12` and print nothing.
The actual length can change with the Python version.
""",
    "template": '''from contextlib import redirect_stdout
from io import StringIO
from types import BuiltinFunctionType


def get_len_help_text(builtin):
    """Return the character count of captured help output."""
    pass
''',
    "tests": '''import builtins
from contextlib import redirect_stdout
from io import StringIO
import sys

import pytest

from helplen import get_len_help_text


@pytest.mark.parametrize("value", [len, max, pow, [].append, "".upper])
def test_accepts_builtin_functions_and_bound_methods(value, monkeypatch, capsys):
    calls = []
    def help_stub(item):
        calls.append(item)
        print("Length help")
    monkeypatch.setattr(builtins, "help", help_stub)
    stream = sys.stdout
    assert get_len_help_text(value) == 12
    assert calls == [value]
    assert sys.stdout is stream
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("text", ["", "x", "a\\nb\\n", "é漢😀\\n"])
def test_counts_characters_exactly(text, monkeypatch, capsys):
    def help_stub(item):
        print(text, end="")
    monkeypatch.setattr(builtins, "help", help_stub)
    assert get_len_help_text(len) == len(text)
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("value", [int, list, str, "len", 1, None, lambda: None, str.upper])
def test_rejects_other_objects_before_help(value, monkeypatch):
    calls = []
    monkeypatch.setattr(builtins, "help", lambda item: calls.append(item))
    stream = sys.stdout
    with pytest.raises(ValueError):
        get_len_help_text(value)
    assert calls == []
    assert sys.stdout is stream


def test_actual_help_matches_independent_capture(capsys):
    expected = StringIO()
    with redirect_stdout(expected):
        help(pow)
    stream = sys.stdout
    assert expected.getvalue()
    assert get_len_help_text(pow) == len(expected.getvalue())
    assert sys.stdout is stream
    assert capsys.readouterr().out == ""


def test_help_exception_restores_stdout(monkeypatch, capsys):
    def broken_help(item):
        print("partial output")
        raise RuntimeError("help failed")
    monkeypatch.setattr(builtins, "help", broken_help)
    stream = sys.stdout
    with pytest.raises(RuntimeError, match="help failed"):
        get_len_help_text(len)
    assert sys.stdout is stream
    assert capsys.readouterr().out == ""
    monkeypatch.setattr(builtins, "help", lambda item: print("ok"))
    assert get_len_help_text(max) == 3
    assert sys.stdout is stream
    print("still connected")
    assert capsys.readouterr().out == "still connected\\n"
''',
    "reference": '''from contextlib import redirect_stdout
from io import StringIO
import sys
from types import BuiltinFunctionType


def get_len_help_text(builtin):
    if not isinstance(builtin, BuiltinFunctionType):
        raise ValueError("expected a built-in function")
    output = StringIO()
    with redirect_stdout(output):
        help(builtin)
    return len(output.getvalue())
''',
    "mutations": [
        {"name": "accept_any_callable", "old": "isinstance(builtin, BuiltinFunctionType)", "new": "callable(builtin)"},
        {"name": "count_bytes_instead_of_characters", "old": "len(output.getvalue())", "new": "len(output.getvalue().encode())"},
        {"name": "leak_help_output", "old": "redirect_stdout(output)", "new": "redirect_stdout(sys.stdout)"},
        {"name": "strip_output_whitespace", "old": "len(output.getvalue())", "new": "len(output.getvalue().strip())"},
    ],
    "examples": [{"input": 'get_len_help_text(len), when help writes "Length help\\n"', "output": "12"}],
    "notes": "The premium template and tests were not visible. These are recreated. "
             "Tests use deterministic help stubs and independently capture actual help output.",
    "original": False,
}
