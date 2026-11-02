## Reference solution

Use this implementation above the supplied tests and runner.

```python
from functools import wraps

# FOCUS: write the decorator by hand: @wraps(func), a wrapper with *args/**kwargs,
#        check each positional argument, then call func.
# SUPPLIED: _check_arg does the type and range check. It is not the skill of
#        this exercise. Use it. Do not edit it.


def _check_arg(value):
    """Raise TypeError for a non-int (bool too). Raise ValueError for a negative int."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError('positional arguments must be integers')
    if value < 0:
        raise ValueError('positional arguments must be nonnegative')



def validate_int_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for value in args:
            _check_arg(value)
        return func(*args, **kwargs)
    return wrapper
```
