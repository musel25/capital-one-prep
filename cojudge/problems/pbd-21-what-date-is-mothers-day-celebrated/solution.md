## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import date, timedelta
def get_mothers_day_date(year):
    first = date(year, 5, 1)
    return first + timedelta(days=(6 - first.weekday()) % 7 + 7)
```
