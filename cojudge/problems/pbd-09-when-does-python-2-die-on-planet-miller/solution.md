## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import datetime
BITE_CREATED_DT = datetime(2018, 2, 26)
PY2_DEATH_DT = datetime(2020, 1, 1)
def calc_hours_left(start=BITE_CREATED_DT, end=PY2_DEATH_DT):
    if end < start:
        raise ValueError('Reversed dates')
    return (end - start).total_seconds() / 3600
def calc_minutes_miller(start=BITE_CREATED_DT, end=PY2_DEATH_DT):
    return calc_hours_left(start, end) / (365 * 24 * 7) * 60
```
