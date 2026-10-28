## Reference solution

Paste this code above the supplied tests and runner.

```python
from enum import Enum
from datetime import datetime
class DateFormat(Enum):
    EU = '%d/%m/%Y'
    US = '%m/%d/%Y'
    ISO = '%Y-%m-%d'
class InfDateFmtError(ValueError):
    pass
def get_dates(values):
    formats = [item.value for item in DateFormat]
    counts = dict.fromkeys(formats, 0)
    parsed = []
    invalid = 0
    for value in values:
        matches = {}
        for pattern in formats:
            try:
                matches[pattern] = datetime.strptime(value, pattern)
                counts[pattern] += 1
            except (ValueError, TypeError):
                pass
        parsed.append(matches)
        invalid += not bool(matches)
    best = max(counts.values(), default=0)
    winners = [pattern for pattern, count in counts.items() if count == best]
    if not best or len(winners) != 1 or invalid > best:
        raise InfDateFmtError('Cannot infer a unique format')
    pattern = winners[0]
    return [row[pattern].date().isoformat() if pattern in row else 'Invalid' for row in parsed]
```
