## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import datetime
NOW = datetime(2019, 3, 20, 12)
TIME_OFFSETS = ((86400, 'day'), (3600, 'hour'), (60, 'minute'), (1, 'second'))
def pretty_date(value, now=NOW):
    if not isinstance(value, datetime) or value > now:
        raise ValueError('Expected a past datetime')
    seconds = (now - value).total_seconds()
    if seconds > 172800:
        return value.strftime('%m/%d/%y')
    for size, unit in TIME_OFFSETS:
        count = int(seconds // size)
        if count:
            return f'{count} {unit}{"s" if count != 1 else ""} ago'
    return 'just now'
```
