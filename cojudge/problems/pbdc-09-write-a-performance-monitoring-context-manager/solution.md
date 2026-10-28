## Reference solution

Use this implementation above the supplied tests and runner.

```python
import contextlib
import time
from collections import Counter
from datetime import date

OPERATION_THRESHOLD_IN_SECONDS = 2.2
ALERT_THRESHOLD = 3
ALERT_MSG = 'ALERT: suffering performance hit today'
violations = Counter()


@contextlib.contextmanager
def timeit():
    started = time.perf_counter()
    try:
        yield
    finally:
        duration = time.perf_counter() - started
        if duration >= OPERATION_THRESHOLD_IN_SECONDS:
            today = date.today()
            violations[today] += 1
            if violations[today] >= ALERT_THRESHOLD:
                print(ALERT_MSG)
```
