## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import date, timedelta
TODAY = date(2019, 1, 1)
def get_hundred_weekdays(start_date=TODAY):
    result = []
    current = start_date
    while len(result) < 100:
        if current.weekday() < 5:
            result.append(current)
        current += timedelta(days=1)
    return result
```
