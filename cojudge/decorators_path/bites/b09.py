"""Recreated performance monitor exercise; no premium source code used."""

SPEC = {
    "title": "Write a performance monitoring context manager",
    "module": "performance",
    "contract": "Expose OPERATION_THRESHOLD_IN_SECONDS=2.2, ALERT_THRESHOLD=3, "
                "ALERT_MSG='ALERT: suffering performance hit today', and violations as a collections.Counter. "
                "timeit() is a contextlib.contextmanager that yields None. Measure elapsed seconds with "
                "time.perf_counter() at entry and exit. A duration >= 2.2 is a violation. Count violations "
                "under date.today() at exit. For every violating operation with that day's count >= 3, "
                "print ALERT_MSG once. A faster operation never alerts. Dates have independent counts. "
                "Always measure and record on exit, including when the block raises. Propagate the block's "
                "exception. Import time and from datetime import date so the clock and date can be replaced in tests.",
    "statement": """Implement `timeit()` in `performance` to track slow operations by date.

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
""",
    "template": '''import contextlib
import time
from collections import Counter
from datetime import date

OPERATION_THRESHOLD_IN_SECONDS = 2.2
ALERT_THRESHOLD = 3
ALERT_MSG = 'ALERT: suffering performance hit today'
violations = Counter()


@contextlib.contextmanager
def timeit():
    # Record elapsed time and update the exit date's count.
    yield
''',
    "tests": '''from collections import Counter
from datetime import date as real_date
from types import SimpleNamespace

import pytest
import performance


@pytest.fixture
def clock(monkeypatch):
    performance.violations.clear()
    state = SimpleNamespace(now=0.0, day=real_date(2026, 10, 28))
    monkeypatch.setattr(performance.time, 'perf_counter', lambda: state.now)
    monkeypatch.setattr(performance, 'date', SimpleNamespace(today=lambda: state.day))
    return state


def operate(clock, seconds):
    with performance.timeit() as result:
        assert result is None
        clock.now += seconds


def test_public_configuration_and_counter(clock):
    assert performance.OPERATION_THRESHOLD_IN_SECONDS == 2.2
    assert performance.ALERT_THRESHOLD == 3
    assert performance.ALERT_MSG == 'ALERT: suffering performance hit today'
    assert isinstance(performance.violations, Counter)


def test_exact_threshold_counts_as_violation(clock, capsys):
    operate(clock, 2.2)
    assert performance.violations == {clock.day: 1}
    assert capsys.readouterr().out == ''


def test_faster_operations_do_not_count(clock, capsys):
    for duration in (0, 0.1, 2.19):
        operate(clock, duration)
    assert performance.violations == {}
    assert capsys.readouterr().out == ''


def test_alert_starts_on_third_violation(clock, capsys):
    for expected in (1, 2):
        operate(clock, 3)
        assert performance.violations[clock.day] == expected
        assert capsys.readouterr().out == ''
    operate(clock, 3)
    assert performance.violations[clock.day] == 3
    assert capsys.readouterr().out == performance.ALERT_MSG + '\\n'


def test_each_later_violation_alerts_but_fast_operations_do_not(clock, capsys):
    performance.violations[clock.day] = 3
    operate(clock, 4)
    operate(clock, 1)
    operate(clock, 5)
    assert performance.violations[clock.day] == 5
    assert capsys.readouterr().out == (performance.ALERT_MSG + '\\n') * 2


def test_dates_keep_independent_counts(clock, capsys):
    first = clock.day
    performance.violations[first] = 3
    clock.day = real_date(2026, 10, 29)
    operate(clock, 3)
    assert performance.violations == {first: 3, clock.day: 1}
    assert capsys.readouterr().out == ''
    clock.day = first
    operate(clock, 3)
    assert performance.violations[first] == 4
    assert capsys.readouterr().out == performance.ALERT_MSG + '\\n'


def test_operation_crossing_midnight_uses_exit_date(clock, capsys):
    entry_day = clock.day
    exit_day = real_date(2026, 10, 29)
    performance.violations[exit_day] = 2
    with performance.timeit():
        clock.now += 3
        clock.day = exit_day
    assert performance.violations == {exit_day: 3}
    assert entry_day not in performance.violations
    assert capsys.readouterr().out == performance.ALERT_MSG + '\\n'


@pytest.mark.parametrize('error_type', [ValueError, KeyboardInterrupt])
def test_failed_slow_operation_is_counted_and_error_propagates(clock, capsys, error_type):
    failure = error_type('operation failed')
    performance.violations[clock.day] = 2
    with pytest.raises(error_type) as caught:
        with performance.timeit():
            clock.now += 3
            raise failure
    assert caught.value is failure
    assert performance.violations[clock.day] == 3
    assert capsys.readouterr().out == performance.ALERT_MSG + '\\n'


def test_failed_fast_operation_is_not_counted(clock, capsys):
    with pytest.raises(RuntimeError, match='fast failure'):
        with performance.timeit():
            clock.now += 1
            raise RuntimeError('fast failure')
    assert performance.violations == {}
    assert capsys.readouterr().out == ''


def test_nested_operations_use_their_own_entry_time(clock, capsys):
    with performance.timeit():
        clock.now += 1
        with performance.timeit():
            clock.now += 1
        clock.now += 1
    assert performance.violations == {clock.day: 1}
    assert capsys.readouterr().out == ''
''',
    "reference": '''import contextlib
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
''',
    "mutations": [
        {"name": "exclusive_duration_threshold", "old": "duration >= OPERATION_THRESHOLD_IN_SECONDS", "new": "duration > OPERATION_THRESHOLD_IN_SECONDS"},
        {"name": "only_third_violation_alerts", "old": "violations[today] >= ALERT_THRESHOLD", "new": "violations[today] == ALERT_THRESHOLD"},
        {"name": "failed_operations_not_measured", "old": "    finally:\n", "new": "    except BaseException:\n        raise\n    else:\n"},
        {"name": "each_operation_resets_daily_count", "old": "violations[today] += 1", "new": "violations[today] = 1"},
        {"name": "entry_date_instead_of_exit_date", "old": "    started = time.perf_counter()\n    try:\n        yield\n    finally:\n        duration = time.perf_counter() - started\n        if duration >= OPERATION_THRESHOLD_IN_SECONDS:\n            today = date.today()", "new": "    started = time.perf_counter()\n    entry_date = date.today()\n    try:\n        yield\n    finally:\n        duration = time.perf_counter() - started\n        if duration >= OPERATION_THRESHOLD_IN_SECONDS:\n            today = entry_date"},
    ],
    "examples": [{"input": "Three operations of 2.2 seconds on the same date", "output": "ALERT: suffering performance hit today", "explanation": "The third violation reaches the daily alert threshold."}],
    "notes": "Recreated local API. Every later violation alerts. Counts use the exit date. Tests use a fake clock and date; no waiting is required.",
    "original": False,
}
