## Reference solution

```python
from datetime import datetime, timezone


def count_utc_days(timestamps):
    counts = {}
    for timestamp in timestamps:
        parsed = datetime.fromisoformat(timestamp)
        day = parsed.astimezone(timezone.utc).date().isoformat()
        counts[day] = counts.get(day, 0) + 1
    return counts
```
