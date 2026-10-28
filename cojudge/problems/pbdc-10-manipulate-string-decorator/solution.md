## Reference solution

Use this implementation above the supplied tests and runner.

```python
from functools import wraps


def strip_range(start, end):
    def decorate(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            text = func(*args, **kwargs)
            return ''.join('.' if start <= index < end else char
                           for index, char in enumerate(text))
        return wrapped
    return decorate
```
