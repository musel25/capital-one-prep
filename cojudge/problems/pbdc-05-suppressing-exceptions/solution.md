## Reference solution

Use this implementation above the supplied tests and runner.

```python
from contextlib import suppress


def sum_numbers(numbers):
    total = 0
    for value in numbers:
        with suppress(TypeError, ValueError):
            total += int(value)
    return total
```
