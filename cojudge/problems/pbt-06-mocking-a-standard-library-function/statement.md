# 06. Mocking a standard library function

Write **tests**, not the implementation. [Original Pybites exercise](https://pybitesplatform.com/bites/mocking-a-standard-library-function/).

This is an offline recreation from the public description. The original code and template are premium and were not available. The API below belongs to this recreation.

## Contract

gen_hex_color() yields indefinitely. Each next() calls colors.sample(HEX, 6), where HEX is 0123456789ABCDEF. Join the sampled characters without changes and prepend #. Patch colors.sample to make tests deterministic. Check successive yields and the sample arguments.

## Code to test

Import this module as `colors`. The judge supplies it automatically.

```python
from random import sample

HEX = '0123456789ABCDEF'

def gen_hex_color():
    while True:
        yield '#' + ''.join(sample(HEX, 6))
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
