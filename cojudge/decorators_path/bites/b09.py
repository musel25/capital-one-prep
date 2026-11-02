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
    # TODO: measure with time.perf_counter() and call _record(duration) on exit.
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
''',
    "hints": [
        "Focus: @contextlib.contextmanager. Code before yield runs on entry; code after yield runs on exit.",
        "Put yield inside try and call _record in finally, so a failed block is also measured.",
        "Use time.perf_counter() (call it through the time module, so the tests can replace the clock).",
    ],
    "mutations": [
        {"name": "failed_operations_not_measured", "old": "    finally:\n", "new": "    except BaseException:\n        raise\n    else:\n"},
        {"name": "reversed_duration", "old": "_record(time.perf_counter() - started)", "new": "_record(started - time.perf_counter())"},
        {"name": "never_records", "old": "        _record(time.perf_counter() - started)", "new": "        pass"},
        {"name": "exception_swallowed", "old": "    try:\n        yield\n    finally:\n        _record(time.perf_counter() - started)", "new": "    try:\n        yield\n    except Exception:\n        pass\n    finally:\n        _record(time.perf_counter() - started)"},
    ],
    "examples": [{"input": "Three operations of 2.2 seconds on the same date", "output": "ALERT: suffering performance hit today", "explanation": "The third violation reaches the daily alert threshold."}],
    "notes": "Recreated local API. Every later violation alerts. Counts use the exit date. Tests use a fake clock and date; no waiting is required.",
    "original": False,
}
