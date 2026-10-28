## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import date
START_DATE = date(2018, 11, 1)
def get_months_passed(year, month, day):
    end = date(year, month, day)
    if end < START_DATE:
        raise ValueError('End before start')
    months = (end.year - START_DATE.year) * 12 + end.month - START_DATE.month
    return months + (end.day - START_DATE.day >= 10)
```
