## Reference solution

Use this implementation above the supplied tests and runner.

```python
from functools import wraps


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
```
