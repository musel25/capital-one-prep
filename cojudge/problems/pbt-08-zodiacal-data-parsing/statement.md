# 08. Zodiacal data parsing

Write **tests**, not the implementation. [Original Pybites exercise](https://pybitesplatform.com/bites/zodiacal-data-parsing/).

This is an offline recreation from the public description. The original code and template are premium and were not available. The API below belongs to this recreation.

## Contract

Use the supplied static 12-sign data. get_signs() returns independent copies. get_sign_with_most_famous_people(signs) returns the name with the largest list; ties use the first item; empty input raises ValueError. signs_are_mutually_compatible requires both directions and exact names; unknown names raise KeyError. get_sign_by_date(signs, day) accepts datetime.date. Endpoints are inclusive. Capricorn spans the year boundary. No matching date raises ValueError. The data is constructed for practice.

## Code to test

Import this module as `zodiac`. The judge supplies it automatically.

```python
from datetime import date

# Small static data set for offline parsing and date-boundary practice.
DATA = [
    {'name': 'Aries', 'start': (3, 21), 'end': (4, 19), 'famous_people': ['A', 'B'], 'compatible': ['Leo']},
    {'name': 'Taurus', 'start': (4, 20), 'end': (5, 20), 'famous_people': ['C'], 'compatible': ['Virgo']},
    {'name': 'Gemini', 'start': (5, 21), 'end': (6, 20), 'famous_people': ['D'], 'compatible': ['Libra']},
    {'name': 'Cancer', 'start': (6, 21), 'end': (7, 22), 'famous_people': ['E'], 'compatible': ['Pisces']},
    {'name': 'Leo', 'start': (7, 23), 'end': (8, 22), 'famous_people': ['F', 'G', 'H'], 'compatible': ['Aries']},
    {'name': 'Virgo', 'start': (8, 23), 'end': (9, 22), 'famous_people': [], 'compatible': ['Taurus']},
    {'name': 'Libra', 'start': (9, 23), 'end': (10, 22), 'famous_people': [], 'compatible': []},
    {'name': 'Scorpio', 'start': (10, 23), 'end': (11, 21), 'famous_people': [], 'compatible': []},
    {'name': 'Sagittarius', 'start': (11, 22), 'end': (12, 21), 'famous_people': [], 'compatible': []},
    {'name': 'Capricorn', 'start': (12, 22), 'end': (1, 19), 'famous_people': [], 'compatible': []},
    {'name': 'Aquarius', 'start': (1, 20), 'end': (2, 18), 'famous_people': [], 'compatible': []},
    {'name': 'Pisces', 'start': (2, 19), 'end': (3, 20), 'famous_people': [], 'compatible': ['Cancer']},
]

def get_signs():
    from copy import deepcopy
    return deepcopy(DATA)

def get_sign_with_most_famous_people(signs):
    return max(signs, key=lambda sign: len(sign['famous_people']))['name']

def signs_are_mutually_compatible(signs, first, second):
    by_name = {sign['name']: sign for sign in signs}
    return (second in by_name[first]['compatible']
            and first in by_name[second]['compatible'])

def get_sign_by_date(signs, day):
    value = (day.month, day.day)
    for sign in signs:
        start, end = sign['start'], sign['end']
        if start <= end:
            matches = start <= value <= end
        else:
            matches = value >= start or value <= end
        if matches:
            return sign['name']
    raise ValueError('date has no matching sign')
```

## Your task

Scroll to **WRITE YOUR TESTS BELOW** in the editor. Replace the placeholder with `test_` functions. Keep the supplied target, runner, and adapter unchanged.

1. All tests must pass against the correct code.
2. Cover at least 90% of executable statements in the supplied target.
3. Detect every supplied faulty variant. A faulty variant is detected when at least one test fails against it.

**Run** checks the baseline and the first two faults. **Submit** checks the baseline and all 6 faults. `SURVIVED` identifies a fault your tests missed. A baseline failure shows the test name and error. Empty suites do not pass.

## Offline pytest support

The supplied runner implements the same small pytest subset used by the OOP course: `pytest.raises` (with `match`), `pytest.mark.parametrize`, function and yield fixtures, `pytest.approx` for numbers, `pytest.fail`, `capsys` / `capfd` for Python output, `monkeypatch`, and `tmp_path`. Standard-library `unittest.mock.patch` also works. Use function-scoped fixtures and top-level test functions. Plugins, async tests, pytest classes with setup hooks, skip/xfail, and advanced fixture scopes are not supported.

The judge uses Python 3.11 and no network. This runner measures statement coverage with Python tracing and uses explicit faulty variants. It does **not** run pytest-cov or mutatest. Its acceptance result is specific to this course.

For an older saved tab, use **+** to open the current template. Keep the old tab intact.
