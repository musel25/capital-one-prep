## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import date, timedelta
import re
TODAY = date(2018, 11, 12)
def extract_dates(text):
    return [date.fromisoformat(value) for value in re.findall(r'^\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|', text, re.M)]
def calculate_streak(dates, today=TODAY):
    present = set(dates)
    current = today if today in present else today - timedelta(days=1)
    count = 0
    while current in present:
        count += 1
        current -= timedelta(days=1)
    return count
```
