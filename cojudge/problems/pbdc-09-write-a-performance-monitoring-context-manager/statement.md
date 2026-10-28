# 09. Write a performance monitoring context manager

Implement `timeit()` in `performance` to track slow operations by date.

Use `@contextlib.contextmanager`. Measure each operation with
`time.perf_counter()` at entry and exit. The context manager yields `None`.
An operation that takes at least `OPERATION_THRESHOLD_IN_SECONDS = 2.2` seconds
increases the public `violations` counter under `date.today()` at **exit**.
Keep `violations` as a `collections.Counter`. Each date has an independent count.

Use `ALERT_THRESHOLD = 3`. Print `ALERT_MSG` once on the third violation and on
every later violation that day. Fast operations do not increase the counter or
print an alert. Record failed operations too, then propagate their error.
Nested operations must each measure their own duration.

For example, three operations that each take `2.2` seconds on one date produce:

```text
ALERT: suffering performance hit today
```

Keep `ALERT_MSG = 'ALERT: suffering performance hit today'`. Use `import time`
and `from datetime import date` so tests can replace the clock and date.
