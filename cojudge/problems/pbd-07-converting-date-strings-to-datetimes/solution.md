## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import datetime
from collections import Counter
def convert_to_datetime(value):
    return datetime.strptime(value.rsplit(' ', 1)[0], '%a, %d %b %Y %H:%M:%S')
def get_month_most_posts(dates):
    counts = Counter(f'{d.year:04}-{d.month:02}' for d in dates)
    if not counts:
        raise ValueError('No dates')
    return min(counts, key=lambda month: (-counts[month], month))
```
