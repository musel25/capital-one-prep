## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import datetime, timedelta
PYBITES_BORN = datetime(2016, 12, 19)
def gen_special_pybites_dates():
    current = PYBITES_BORN
    while True:
        current += timedelta(days=100)
        yield current
```
