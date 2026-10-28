In this Bite we will write tests for a module that parses data from Zodiacal / The Zodiac API (update 2025: this site is no longer online, but don't worry, we use a static copy for this exercise). See the CODE TO TEST tab below. The get_signs function is used in the signs fixture that has been provided in the template. You can use it in your tests by passing it into your test functions (read our article if you have not used them yet). Write code to test get_sign_with_most_famous_people, signs_are_mutually_compatible and get_sign_by_date.

As with all our test Bites, your test code will be tested for: 1. correct syntax, 2. pytest passes all tests, 3. test coverage, and 4. mutation score (mutatest)

Good luck and keep calm and code in Python + pytest!

For this version, write tests for the supplied code. Your tests must pass against the correct code, cover at least 90% of its executable statements, and detect every supplied faulty version. A fault is detected when at least one test fails. An empty test suite does not pass.

Import the target as `zodiac`. The judge supplies it automatically.

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
