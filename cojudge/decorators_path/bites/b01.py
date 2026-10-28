"""Sandwich decorator: recreated template and tests from the public description."""

SPEC = {
    "title": "Create a sandwich decorator",
    "module": "sandwich",
    "original": False,
    "contract": (
        "sandwich(func) returns a callable. Each call prints UPPER_SLICE before "
        "calling func and LOWER_SLICE after a successful call. Forward all args "
        "and kwargs once. Return the same result object. Preserve function name, "
        "docstring and annotations. Propagate the original exception. Printing "
        "the lower slice when func raises is optional."
    ),
    "statement": '''Implement `sandwich(func)`.

The decorated function prints the upper bread slice first. It then calls the
wrapped function. After a successful call, it prints the lower bread slice.
Use the supplied constants. Forward all positional and keyword arguments.
Return the wrapped result. Preserve the function name, docstring and annotations.
Let exceptions from the wrapped function reach the caller. The lower slice is
optional when the wrapped function raises.

Example: a decorated function that prints `cheese` produces:

```text
=== Upper bread slice ===
cheese
=== Lower bread slice ===
```
''',
    "template": '''UPPER_SLICE = "=== Upper bread slice ==="
LOWER_SLICE = "=== Lower bread slice ==="


def sandwich(func):
    """Add bread output around a function call."""
    # TODO: return the decorated function.
    pass
''',
    "tests": '''import pytest

from sandwich import LOWER_SLICE, UPPER_SLICE, sandwich


def test_constants_have_the_required_text():
    assert UPPER_SLICE == "=== Upper bread slice ==="
    assert LOWER_SLICE == "=== Lower bread slice ==="


def test_output_surrounds_the_wrapped_call(capsys):
    @sandwich
    def filling():
        print("cheese")
    assert filling() is None
    assert capsys.readouterr().out == (
        "=== Upper bread slice ===\\ncheese\\n=== Lower bread slice ===\\n"
    )


def test_forwards_arguments_once_and_returns_the_same_object(capsys):
    calls = []
    answer = {"filling": "egg"}
    @sandwich
    def order(first, *extras, sauce):
        calls.append((first, extras, sauce))
        return answer
    assert order("egg", "salad", "cheese", sauce="hot") is answer
    assert calls == [("egg", ("salad", "cheese"), "hot")]
    assert capsys.readouterr().out == UPPER_SLICE + "\\n" + LOWER_SLICE + "\\n"


def test_preserves_function_metadata():
    def filling(count: int) -> str:
        """Choose the filling."""
        return str(count)
    decorated = sandwich(filling)
    assert decorated.__name__ == "filling"
    assert decorated.__doc__ == "Choose the filling."
    assert decorated.__annotations__ == {"count": int, "return": str}


def test_decoration_does_not_call_the_function_or_print(capsys):
    calls = []
    def filling():
        calls.append("called")
    decorated = sandwich(filling)
    assert callable(decorated)
    assert calls == []
    assert capsys.readouterr().out == ""


def test_repeated_calls_and_separate_wrappers_keep_no_result_state(capsys):
    @sandwich
    def echo(value):
        return value
    @sandwich
    def other(value):
        return value + 10
    assert echo(0) == 0
    assert other(2) == 12
    assert echo(3) == 3
    assert capsys.readouterr().out == (UPPER_SLICE + "\\n" + LOWER_SLICE + "\\n") * 3


def test_propagates_the_original_exception(capsys):
    error = ValueError("bad filling")
    calls = []
    @sandwich
    def reject(value):
        calls.append(value)
        raise error
    with pytest.raises(ValueError) as caught:
        reject("spoiled")
    assert caught.value is error
    assert calls == ["spoiled"]
    assert capsys.readouterr().out.startswith(UPPER_SLICE + "\\n")
''',
    "examples": [{
        "input": "@sandwich\ndef filling():\n    print('cheese')\nfilling()",
        "output": "=== Upper bread slice ===\ncheese\n=== Lower bread slice ===",
        "explanation": "The bread lines surround the wrapped output.",
    }],
    "notes": "The template and tests are recreated from the public description. This course also requires argument forwarding, result identity and function metadata preservation.",
}

SPEC["reference"] = '''from functools import wraps

UPPER_SLICE = "=== Upper bread slice ==="
LOWER_SLICE = "=== Lower bread slice ==="


def sandwich(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(UPPER_SLICE)
        result = func(*args, **kwargs)
        print(LOWER_SLICE)
        return result
    return wrapper
'''
SPEC["mutations"] = [
    {"name": "omit the lower bread slice", "old": "        print(LOWER_SLICE)\n", "new": ""},
    {"name": "discard the result", "old": "return result", "new": "return None"},
    {"name": "drop keyword arguments", "old": "func(*args, **kwargs)", "new": "func(*args)"},
    {"name": "call the wrapped function twice", "old": "result = func(*args, **kwargs)", "new": "result = func(*args, **kwargs)\n        func(*args, **kwargs)"},
    {"name": "lose function metadata", "old": "    @wraps(func)\n", "new": ""},
]
