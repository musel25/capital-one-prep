## How it works

Parse each timestamp into an aware datetime, convert it to UTC, and take the date. Then count with a dictionary.

## Common mistakes

- Taking the date from the text (`timestamp[:10]`). That is the local date.
- Replacing the offset instead of converting the time.
- Overwriting a count instead of adding one.

## Solution

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
