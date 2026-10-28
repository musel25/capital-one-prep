"""Integer validation decorator: recreated from the public description."""

SPEC = {
    "title": "Write a numbers validation decorator",
    "module": "validation",
    "original": False,
    "contract": (
        "validate_int_args(func) validates each positional argument from left to "
        "right before calling func. Reject bool and other non-int values with "
        "TypeError. Reject a negative int with ValueError. Zero and positive "
        "integers are allowed. Forward keyword arguments unchanged without "
        "validation. Call func once after validation, return its same result "
        "and propagate its exceptions. Preserve function name, docstring and annotations. "
        "No positional arguments is valid. Error message text is not specified."
    ),
    "statement": '''Implement `validate_int_args(func)`.

Check each positional argument from left to right before you call the wrapped
function. Raise `TypeError` for a non-integer. Raise `ValueError` for a negative
integer. Zero is valid. In this course, `bool` is not a valid integer.

Do not validate keyword arguments. Forward them unchanged. Call the wrapped
function once after successful validation. Return its result. Preserve its
name, docstring and annotations. Propagate its exceptions.

```python
@validate_int_args
def total(*values, label='sum'):
    return label, sum(values)

total(0, 2, 3, label='count')  # ('count', 5)
total(-1)                    # raises ValueError
total(True)                  # raises TypeError
```
''',
    "template": '''def validate_int_args(func):
    """Allow only nonnegative integers in positional arguments."""
    # TODO: return the decorated function.
    pass
''',
    "tests": '''import pytest

from validation import validate_int_args


def test_allows_zero_positive_and_large_integers():
    @validate_int_args
    def total(*values):
        return sum(values)
    assert total() == 0
    assert total(0) == 0
    assert total(0, 2, 3) == 5
    assert total(10 ** 40, 1) == 10 ** 40 + 1


@pytest.mark.parametrize("bad", [True, False, 1.0, -1.5, "3", None, [], {}])
def test_rejects_non_integers_without_calling_the_function(bad):
    calls = []
    @validate_int_args
    def record(*values):
        calls.append(values)
    with pytest.raises(TypeError):
        record(1, bad, 2)
    assert calls == []


@pytest.mark.parametrize("values", [(-1,), (0, -1), (2, 3, -10)])
def test_rejects_negative_integers_before_the_function_runs(values):
    calls = []
    @validate_int_args
    def record(*values):
        calls.append(values)
    with pytest.raises(ValueError):
        record(*values)
    assert calls == []


def test_checks_arguments_from_left_to_right():
    @validate_int_args
    def total(*values):
        return sum(values)
    with pytest.raises(ValueError):
        total(-1, "bad")
    with pytest.raises(TypeError):
        total("bad", -1)


def test_keywords_are_forwarded_unchanged_and_are_not_validated():
    calls = []
    data = ["payload"]
    answer = {"ok": True}
    @validate_int_args
    def record(*values, **options):
        calls.append((values, options))
        return answer
    assert record(1, 0, negative=-2, flag=True, data=data) is answer
    assert calls == [((1, 0), {"negative": -2, "flag": True, "data": ["payload"]})]
    assert calls[0][1]["data"] is data
    assert record(value="not an integer") is answer
    assert calls[1] == ((), {"value": "not an integer"})


def test_preserves_function_metadata():
    def total(value: int) -> int:
        """Return the count."""
        return value
    wrapped = validate_int_args(total)
    assert wrapped.__name__ == "total"
    assert wrapped.__doc__ == "Return the count."
    assert wrapped.__annotations__ == {"value": int, "return": int}


def test_repeated_calls_and_wrappers_keep_no_validation_or_result_state():
    @validate_int_args
    def first(value):
        return value + 1
    @validate_int_args
    def second(value):
        return value + 10
    assert first(1) == 2
    with pytest.raises(TypeError):
        first("bad")
    with pytest.raises(ValueError):
        first(-1)
    assert second(2) == 12
    assert first(0) == 1
    assert first(3) == 4


def test_decoration_does_not_call_the_wrapped_function():
    calls = []
    def record():
        calls.append("called")
    wrapped = validate_int_args(record)
    assert callable(wrapped)
    assert calls == []


def test_wrapped_exceptions_reach_the_caller_unchanged():
    error = LookupError("not found")
    @validate_int_args
    def find(value):
        raise error
    with pytest.raises(LookupError) as caught:
        find(0)
    assert caught.value is error
''',
    "examples": [
        {"input": "@validate_int_args\ndef total(*values, label='sum'):\n    return label, sum(values)\ntotal(0, 2, 3, label='count')", "output": "('count', 5)"},
        {"input": "total(-1)", "output": "ValueError"},
        {"input": "total(True)", "output": "TypeError"},
    ],
    "notes": "The template and tests are recreated from the public description. This course uses the local API validate_int_args. It explicitly rejects bool, checks left to right, leaves kwargs unvalidated and requires metadata preservation.",
}

SPEC["reference"] = '''from functools import wraps


def validate_int_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for value in args:
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError('positional arguments must be integers')
            if value < 0:
                raise ValueError('positional arguments must be nonnegative')
        return func(*args, **kwargs)
    return wrapper
'''
SPEC["mutations"] = [
    {"name": "accept bool as int", "old": "isinstance(value, bool) or not isinstance(value, int)", "new": "not isinstance(value, int)"},
    {"name": "reject zero", "old": "value < 0", "new": "value <= 0"},
    {"name": "check arguments in reverse order", "old": "for value in args:", "new": "for value in reversed(args):"},
    {"name": "validate keyword values", "old": "for value in args:", "new": "for value in (*args, *kwargs.values()):"},
    {"name": "use the wrong exception for negatives", "old": "raise ValueError('positional arguments must be nonnegative')", "new": "raise TypeError('positional arguments must be nonnegative')"},
    {"name": "drop keyword arguments", "old": "func(*args, **kwargs)", "new": "func(*args)"},
    {"name": "lose function metadata", "old": "    @wraps(func)\n", "new": ""},
]
