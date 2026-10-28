## Reference solution

Use this implementation above the supplied tests and runner.

```python
from functools import singledispatch
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
```
