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

# FOCUS: write the generator context manager by hand: start the clock,
#        yield inside try, and record the time in finally (also when the block raises).
# SUPPLIED: _record does the threshold, the daily count and the alert. It is not
#        the skill of this exercise. Use it. Do not edit it.


def _record(duration):
    """Count a violation for today if duration >= the threshold; print ALERT_MSG from the 3rd one on."""
    if duration >= OPERATION_THRESHOLD_IN_SECONDS:
        today = date.today()
        violations[today] += 1
        if violations[today] >= ALERT_THRESHOLD:
            print(ALERT_MSG)


@contextlib.contextmanager
def timeit():
    started = time.perf_counter()
    try:
        yield
    finally:
        _record(time.perf_counter() - started)
```
