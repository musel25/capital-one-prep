## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import datetime, timedelta
def get_hundred_days_end(start=datetime(2017, 3, 30)):
    return start + timedelta(days=100)
def get_days_between(start=datetime(2016, 12, 19), end=datetime(2018, 5, 8)):
    return (end - start).days
```
