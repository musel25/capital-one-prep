## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import datetime, timedelta
import re
NOW = datetime(2019, 2, 6, 22)
def add_todo(duration, description, start_time=NOW):
    units = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    tokens = duration.split()
    if not tokens:
        raise ValueError('Empty duration')
    seconds = 0
    for token in tokens:
        match = re.fullmatch(r'(\d+)([dhms])', token)
        if not match:
            raise ValueError('Invalid token')
        seconds += int(match[1]) * units[match[2]]
    when = start_time + timedelta(seconds=seconds)
    return f'{description} @ {when.year:04}-{when:%m-%d %H:%M:%S}'
```
