## Reference solution

Use this implementation above the supplied tests and runner.

```python
from functools import wraps

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
```
