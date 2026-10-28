## Reference solution

Use this implementation above the supplied tests and runner.

```python
from functools import wraps


def make_html(tag):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            text = func(*args, **kwargs)
            return f"<{tag}>{text}</{tag}>"
        return wrapper
    return decorate
```
