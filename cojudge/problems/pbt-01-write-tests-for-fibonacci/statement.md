# 01. Write tests for fibonacci

Write **tests**, not the implementation. [Original Pybites exercise](https://pybitesplatform.com/bites/write-tests-for-fibonacci/).

This exercise uses the original Fibonacci code visible on Pybites.

## Contract

Pass integer n. Negative n raises ValueError. fib(0)=0 and fib(1)=1. Higher n follows the Fibonacci recurrence. Test n up to 50.

## Code to test

Import this module as `fibonacci`. The judge supplies it automatically.

```python
from functools import cache

@cache
def fib(n):
   if n < 0:
        raise ValueError
   elif n in (0, 1):
       return n
   else:
       return(fib(n-1) + fib(n-2))
```

## Your task

Scroll to **WRITE YOUR TESTS BELOW** in the editor. Replace the placeholder with `test_` functions. Keep the supplied target, runner, and adapter unchanged.

1. All tests must pass against the correct code.
2. Cover at least 90% of executable statements in the supplied target.
3. Detect every supplied faulty variant. A faulty variant is detected when at least one test fails against it.

**Run** checks the baseline and the first two faults. **Submit** checks the baseline and all 5 faults. `SURVIVED` identifies a fault your tests missed. A baseline failure shows the test name and error. Empty suites do not pass.

## Offline pytest support

The supplied runner implements the same small pytest subset used by the OOP course: `pytest.raises` (with `match`), `pytest.mark.parametrize`, function and yield fixtures, `pytest.approx` for numbers, `pytest.fail`, `capsys` / `capfd` for Python output, `monkeypatch`, and `tmp_path`. Standard-library `unittest.mock.patch` also works. Use function-scoped fixtures and top-level test functions. Plugins, async tests, pytest classes with setup hooks, skip/xfail, and advanced fixture scopes are not supported.

The judge uses Python 3.11 and no network. This runner measures statement coverage with Python tracing and uses explicit faulty variants. It does **not** run pytest-cov or mutatest. Its acceptance result is specific to this course.

For an older saved tab, use **+** to open the current template. Keep the old tab intact.
