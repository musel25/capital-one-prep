## Reference solution

Paste this code above the supplied tests and runner.

```python
from datetime import date, timedelta
def tomorrow(today=None):
    if today is None:
        today = date.today()
    return today + timedelta(days=1)
```
