## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import datetime, timedelta
def get_longest_uptime(text, year=2019):
    events = []
    for line in text.splitlines():
        if not line.strip() or line.split()[0] != 'reboot':
            continue
        parts = line.split()
        stamp = ' '.join(parts[-4:])
        events.append(datetime.strptime(f'{year:04d} {stamp}', '%Y %a %b %d %H:%M'))
    events.sort()
    return max((b - a for a, b in zip(events, events[1:])), default=timedelta(0))
```
