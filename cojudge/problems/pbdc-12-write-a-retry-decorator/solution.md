## Reference solution

Use this implementation above the supplied tests and runner.

```python
from functools import wraps

MAX_RETRIES = 3


class MaxRetriesException(Exception):
    """All allowed attempts failed."""


def retry(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                if attempt == MAX_RETRIES - 1:
                    raise MaxRetriesException('all attempts failed') from error
    return wrapped
```
