"""Recreated singledispatch exercise with explicit local type and order rules."""

SPEC = {
    "title": "The singledispatch countdown challenge",
    "module": "countdown",
    "contract": "Implement count_down(value) with functools.singledispatch. Return None. Render a supported "
                "value as text, then print the text and remove its final character until empty. Accept "
                "nonnegative integers, finite nonnegative floats, and strings. Accept list, tuple, dict, and "
                "set containers whose items (dict keys) are nonnegative integers or strings. Join rendered "
                "items without separators. Keep list/tuple order and dict key insertion order. Sort set items "
                "by str before joining. Dict values do not affect output. Reject bool, negative numbers, "
                "nonfinite floats, unsupported types, invalid container items, and nested containers with "
                "ValueError before printing. Do not change inputs. Empty text or containers print nothing.",
    "statement": """Implement `count_down(value)` with `functools.singledispatch`. Print its rendered
text. Remove the final character and repeat until the text is empty. Return `None`.

Use these local rules:
- Accept nonnegative integers, finite nonnegative floats, and strings.
- For a list or tuple, join the rendered items in their input order.
- For a dictionary, join its keys in insertion order. Ignore its values.
- For a set, sort its items by `str` before joining them.
- Container items must be nonnegative integers or strings. Reject nested containers.
- Raise `ValueError` for unsupported types, booleans, or invalid values before printing.
- Do not change the input. Empty text and empty containers print nothing.

Example: `count_down(12.34)` prints:
```text
12.34
12.3
12.
12
1
```
`count_down([12, \"ab\"])` starts with `12ab`, then prints `12a`, `12`, and `1`.
""",
    "template": '''from functools import singledispatch


@singledispatch
def count_down(value):
    """Print successively shorter text for each supported input type."""
    raise ValueError("unsupported type")

# Register handlers for the supported types.
''',
    "tests": '''import pytest

from countdown import count_down


@pytest.mark.parametrize("value, text", [
    (1234, "1234"), (0, "0"), (12.34, "12.34"), (0.0, "0.0"),
    ("abc", "abc"), ("é漢", "é漢"), ("", ""),
    ([12, "ab"], "12ab"), (("x", 0, "y"), "x0y"),
    ({"b": 99, "a": None, 2: []}, "ba2"), ({2, "a", 10}, "102a"),
    ([], ""), ((), ""), ({}, ""), (set(), ""),
])
def test_prints_character_countdown(value, text, capsys):
    assert count_down(value) is None
    expected = "".join(text[:end] + "\\n" for end in range(len(text), 0, -1))
    assert capsys.readouterr().out == expected


@pytest.mark.parametrize("value", [
    True, False, -1, -0.1, float("inf"), float("-inf"), float("nan"),
    None, 1j, b"abc", frozenset({1}), range(3), object(),
    [True], [False], [-1], [1.5], [[1]], (None,), ({1},),
    {True: 1}, {-1: 1}, {(1,): 2}, {False}, {-1}, {1.5},
])
def test_rejects_invalid_values_before_printing(value, capsys):
    with pytest.raises(ValueError):
        count_down(value)
    assert capsys.readouterr().out == ""


def test_valid_prefix_is_not_printed_before_invalid_item(capsys):
    with pytest.raises(ValueError):
        count_down([12, "good", []])
    assert capsys.readouterr().out == ""


def test_does_not_change_containers(capsys):
    values = [[3, "ab"], (2, "cd"), {"b": [1], "a": None}, {2, "x", 10}]
    saved = [values[0].copy(), values[1], values[2].copy(), values[3].copy()]
    for value in values:
        count_down(value)
        capsys.readouterr()
    assert values == saved


def test_has_registered_dispatch_handlers():
    assert callable(count_down.register)
    fallback = count_down.dispatch(object)
    for kind in (int, float, str, list, tuple, dict, set):
        assert kind in count_down.registry
        assert count_down.dispatch(kind) is not fallback
    assert count_down.dispatch(bytes) is fallback
''',
    "reference": '''from functools import singledispatch
from math import isfinite


def _print_text(text):
    while text:
        print(text)
        text = text[:-1]


def _render_item(value):
    if isinstance(value, str):
        return value
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return str(value)
    raise ValueError("container items must be nonnegative integers or strings")


@singledispatch
def count_down(value):
    raise ValueError("unsupported type")


@count_down.register(int)
def _integer(value):
    if isinstance(value, bool) or value < 0:
        raise ValueError("expected a nonnegative integer")
    _print_text(str(value))


@count_down.register(float)
def _float(value):
    if not isfinite(value) or value < 0:
        raise ValueError("expected a finite nonnegative float")
    _print_text(str(value))


@count_down.register(str)
def _string(value):
    _print_text(value)


@count_down.register(list)
@count_down.register(tuple)
def _sequence(value):
    text = "".join(_render_item(item) for item in value)
    _print_text(text)


@count_down.register(dict)
def _mapping(value):
    text = "".join(_render_item(item) for item in value.keys())
    _print_text(text)


@count_down.register(set)
def _set(value):
    text = "".join(_render_item(item) for item in sorted(value, key=str))
    _print_text(text)
''',
    "mutations": [
        {"name": "omit_final_character", "old": "while text:", "new": "while len(text) > 1:"},
        {"name": "remove_first_character", "old": "text = text[:-1]", "new": "text = text[1:]"},
        {"name": "render_dictionary_values", "old": "value.keys()", "new": "value.values()"},
        {"name": "reverse_set_order", "old": "sorted(value, key=str)", "new": "sorted(value, key=str, reverse=True)"},
        {"name": "accept_boolean_numbers", "old": "if isinstance(value, bool) or value < 0:", "new": "if value < 0:"},
    ],
    "examples": [
        {"input": "count_down(1234)", "output": "1234\n123\n12\n1\n"},
        {"input": 'count_down([12, "ab"])', "output": "12ab\n12a\n12\n1\n"},
    ],
    "notes": "The premium template and tests were not visible. These are recreated. "
             "Container ordering and supported types are explicit local guarantees. "
             "The set type is supported; frozenset is outside the supported types.",
    "original": False,
}
