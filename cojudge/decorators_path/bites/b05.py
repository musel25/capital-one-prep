"""Recreated exercise: suppress expected conversion errors."""

SPEC = {
    "title": "Suppressing exceptions",
    "module": "suppressing",
    "contract": "sum_numbers(numbers) accepts any iterable. Convert each value with int and add successful "
                "conversions. Ignore only TypeError and ValueError from conversion. Other errors propagate. "
                "Support integers, signed numeric strings, floats truncated toward zero, None, invalid strings, "
                "and empty input. Do not change the input.",
    "statement": """Implement `sum_numbers(numbers)`. Use `contextlib.suppress` to skip values that raise
`TypeError` or `ValueError` during `int(value)`. Add each successful conversion.
Let other exceptions propagate. Accept any iterable without changing it.
An empty iterable returns `0`. Floats truncate toward zero.

Example: `sum_numbers([\"10\", None, \"bad\", -2.9, \"+3\"])` returns `11`.
""",
    "template": '''from contextlib import suppress


def sum_numbers(numbers):
    """Add successful int conversions; ignore TypeError and ValueError."""
    pass
''',
    "tests": '''import pytest

from suppressing import sum_numbers


@pytest.mark.parametrize("values, expected", [
    ([], 0), ([1, 2, 3], 6), (["10", "-4", "+2", " 3 "], 11),
    ([2.9, -3.9, 0.1], -1), ([None, "bad", "", "1.2"], 0),
    (["10", None, "bad", -2.9, "+3"], 11),
    (["bad", 4, None, 7, "no", -2], 9),
])
def test_successful_conversions(values, expected):
    assert sum_numbers(values) == expected


def test_accepts_single_pass_iterable():
    values = (value for value in ["1", None, "2", "bad", 3])
    assert sum_numbers(values) == 6


def test_does_not_change_input():
    values = ["1", None, "bad", 2.8]
    saved = values.copy()
    assert sum_numbers(values) == 3
    assert values == saved


def test_custom_conversion_is_used():
    class Number:
        def __int__(self):
            return 8
    assert sum_numbers([Number(), "2"]) == 10


@pytest.mark.parametrize("error", [RuntimeError, OverflowError, KeyboardInterrupt])
def test_other_conversion_errors_propagate(error):
    class Broken:
        def __int__(self):
            raise error("conversion failed")
    with pytest.raises(error, match="conversion failed"):
        sum_numbers([1, Broken(), 2])


def test_iteration_errors_are_not_conversion_errors():
    def numbers():
        yield 2
        raise ValueError("iteration failed")
    with pytest.raises(ValueError, match="iteration failed"):
        sum_numbers(numbers())
''',
    "reference": '''from contextlib import suppress


def sum_numbers(numbers):
    total = 0
    for value in numbers:
        with suppress(TypeError, ValueError):
            total += int(value)
    return total
''',
    "mutations": [
        {"name": "do_not_suppress_value_errors", "old": "suppress(TypeError, ValueError)", "new": "suppress(TypeError)"},
        {"name": "suppress_unexpected_errors", "old": "suppress(TypeError, ValueError)", "new": "suppress(BaseException)"},
        {"name": "replace_total_instead_of_adding", "old": "total += int(value)", "new": "total = int(value)"},
        {"name": "reject_float_conversions", "old": "int(value)", "new": "int(str(value))"},
    ],
    "examples": [{"input": 'sum_numbers(["10", None, "bad", -2.9, "+3"])', "output": "11"}],
    "notes": "The premium template and tests were not visible. These are recreated. "
             "The judge checks behavior. It cannot prove that contextlib.suppress was used.",
    "original": False,
}
