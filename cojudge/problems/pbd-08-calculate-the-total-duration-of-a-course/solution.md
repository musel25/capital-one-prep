## Reference solution

Paste this code above the supplied tests and runner.

```python
import re
def get_total_duration(text):
    total = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.search(r'(?:^|\s)(\d+):([0-5]\d)\s*$', line)
        if not match:
            raise ValueError('Invalid duration')
        total += int(match[1]) * 60 + int(match[2])
    hours, rest = divmod(total, 3600)
    minutes, seconds = divmod(rest, 60)
    return f'{hours:02}:{minutes:02}:{seconds:02}'
```
