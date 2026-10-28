## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import timedelta
def get_misssing_dates(dates):
    present = set(dates)
    if not present:
        return set()
    current, end = min(present), max(present)
    missing = set()
    while current < end:
        if current not in present:
            missing.add(current)
        current += timedelta(days=1)
    return missing
```
