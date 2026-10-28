## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import datetime
from collections import Counter
import re
YEAR_MONTH = '%Y-%m'
def get_min_max_amount_of_commits(log, year=None):
    counts = Counter()
    for line in log.splitlines():
        if not line.strip():
            continue
        stamp, changes = line.split('|', 1)
        if not stamp.strip().startswith('Date:') or not re.fullmatch(r'\d+ files? changed(?:, \d+ insertions?\(\+\))?(?:, \d+ deletions?\(-\))?', changes.strip()):
            raise ValueError('Malformed git stat row')
        dt = datetime.strptime(stamp.strip().removeprefix('Date:').strip(), '%a %b %d %H:%M:%S %Y %z')
        if year is not None and dt.year != year:
            continue
        amount = sum(int(n) for n in re.findall(r'(\d+) (?:insertion|deletion)s?\(', changes))
        counts[f'{dt.year:04}-{dt.month:02}'] += amount
    if not counts:
        return None, None
    low = min(counts, key=lambda month: (counts[month], month))
    high = min(counts, key=lambda month: (-counts[month], month))
    return low, high
```
