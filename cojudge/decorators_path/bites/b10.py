"""Recreated string decorator exercise; no premium source code used."""

SPEC = {
    "title": "Manipulate string decorator",
    "module": "string_decorator",
    "contract": "strip_range(start, end) is a decorator factory. The decorated function returns a str. "
                "Replace each character whose index belongs to range(start, end) and is less than the "
                "string length with '.'. Keep the string length and all other characters unchanged. "
                "start and end are nonnegative ints. An empty or reversed range changes nothing; an end "
                "beyond the string is clipped. Forward positional and keyword arguments. Preserve the "
                "function's metadata and propagate its exceptions. Other argument and return types are outside this exercise.",
    "statement": """Write `strip_range(start, end)` in `string_decorator`.

Decorate a function that returns a string. Replace the characters at the selected
indices with periods. Use the indices in Python's `range(start, end)`: include
`start` and exclude `end`. Ignore indices beyond the string. Keep the original
length and all other characters. Both bounds are nonnegative integers. An empty
or reversed range changes nothing. An empty string stays empty. Treat Unicode
characters as ordinary Python string elements.

For example, a function that returns `"Hello world"`, decorated with
`@strip_range(3, 5)`, returns `"Hel.. world"`.

Call the function once for each invocation. Forward all positional and keyword
arguments and propagate its errors. Preserve its name, docstring, module,
annotations, and `__wrapped__` link. Decorators must also work when stacked.
""",
    "template": '''from functools import wraps


def strip_range(start, end):
    """Replace selected characters in a decorated function's result."""
    raise NotImplementedError
''',
    "tests": '''import pytest

from string_decorator import strip_range


@pytest.mark.parametrize('text, start, end, expected', [
    ('Hello world', 3, 5, 'Hel.. world'),
    ('abcdef', 0, 1, '.bcdef'),
    ('abcdef', 5, 6, 'abcde.'),
    ('abcdef', 0, 6, '......'),
    ('abcdef', 2, 99, 'ab....'),
    ('abcdef', 99, 100, 'abcdef'),
    ('abcdef', 3, 3, 'abcdef'),
    ('abcdef', 5, 2, 'abcdef'),
    ('', 0, 100, ''),
    ('a.b c!', 1, 5, 'a....!'),
    ('café 🐍', 3, 6, 'caf...'),
])
def test_selected_indices_preserve_length(text, start, end, expected):
    @strip_range(start, end)
    def message():
        return text
    actual = message()
    assert actual == expected
    assert len(actual) == len(text)


def test_arguments_are_forwarded_and_function_runs_once():
    calls = []
    @strip_range(1, 3)
    def message(first, second, *, suffix='!'):
        calls.append((first, second, suffix))
        return first + second + suffix
    assert message('ab', 'cd', suffix='?') == 'a..d?'
    assert calls == [('ab', 'cd', '?')]
    assert message('x', 'y') == 'x..'
    assert calls[-1] == ('x', 'y', '!')


def test_metadata_and_wrapped_function_are_preserved():
    def message(value: str = 'abc') -> str:
        """Return the given message."""
        return value
    decorated = strip_range(0, 1)(message)
    assert decorated.__name__ == message.__name__
    assert decorated.__doc__ == message.__doc__
    assert decorated.__module__ == message.__module__
    assert decorated.__annotations__ == message.__annotations__
    assert decorated.__wrapped__ is message


def test_original_error_propagates_once():
    calls = []
    failure = ValueError('missing text')
    @strip_range(1, 2)
    def broken(*, text):
        calls.append(text)
        raise failure
    with pytest.raises(ValueError) as caught:
        broken(text='bad')
    assert caught.value is failure
    assert calls == ['bad']


def test_stacked_decorators_and_repeated_calls():
    @strip_range(0, 1)
    @strip_range(3, 5)
    def message(value):
        return value
    assert message('abcdef') == '.bc..f'
    assert message('xyz') == '.yz'
''',
    "reference": '''from functools import wraps


def strip_range(start, end):
    def decorate(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            text = func(*args, **kwargs)
            return ''.join('.' if start <= index < end else char
                           for index, char in enumerate(text))
        return wrapped
    return decorate
''',
    "mutations": [
        {"name": "inclusive_end", "old": "start <= index < end", "new": "start <= index <= end"},
        {"name": "exclusive_start", "old": "start <= index < end", "new": "start < index < end"},
        {"name": "delete_instead_of_replace", "old": "'.' if start <= index < end", "new": "'' if start <= index < end"},
        {"name": "drop_keyword_arguments", "old": "text = func(*args, **kwargs)", "new": "text = func(*args)"},
        {"name": "lose_metadata", "old": "        @wraps(func)\n", "new": ""},
    ],
    "examples": [{"input": "@strip_range(3, 5) on a function returning 'Hello world'", "output": "Hel.. world", "explanation": "Indices 3 and 4 become periods."}],
    "notes": "Recreated local API. Bounds are nonnegative integers; the end bound is exclusive.",
    "original": False,
}
