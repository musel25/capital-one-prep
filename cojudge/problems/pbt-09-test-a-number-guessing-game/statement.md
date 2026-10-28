# 09. Test a number guessing game

Write **tests**, not the implementation. [Original Pybites exercise](https://pybitesplatform.com/bites/test-a-number-guessing-game/).

This is an offline recreation from the public description. The original code and template are premium and were not available. The API below belongs to this recreation.

## Contract

GuessingGame(secret, max_guesses=5) accepts an integer secret in 1..20 and a positive integer limit; reject booleans. Use the exact validation messages in the supplied code. play() reads input for at most max_guesses attempts. Non-numeric input consumes an attempt. Print Enter a number, Too low, Too high, or You win! as applicable. A win returns True immediately. Exhausted attempts print You lose! The number was N and return False. Mock builtins.input. The default prompt is Guess a number: .

## Code to test

Import this module as `guessing`. The judge supplies it automatically.

```python
class GuessingGame:
    def __init__(self, secret, max_guesses=5):
        if type(secret) is not int or not 1 <= secret <= 20:
            raise ValueError('secret must be an integer from 1 to 20')
        if type(max_guesses) is not int or max_guesses < 1:
            raise ValueError('max_guesses must be a positive integer')
        self.secret, self.max_guesses = secret, max_guesses

    def play(self):
        for _ in range(self.max_guesses):
            text = input('Guess a number: ')
            try:
                guess = int(text)
            except ValueError:
                print('Enter a number')
                continue
            if guess == self.secret:
                print('You win!')
                return True
            if guess < self.secret:
                print('Too low')
            else:
                print('Too high')
        print(f'You lose! The number was {self.secret}')
        return False
```

## Your task

Scroll to **WRITE YOUR TESTS BELOW** in the editor. Replace the placeholder with `test_` functions. Keep the supplied target, runner, and adapter unchanged.

1. All tests must pass against the correct code.
2. Cover at least 90% of executable statements in the supplied target.
3. Detect every supplied faulty variant. A faulty variant is detected when at least one test fails against it.

**Run** checks the baseline and the first two faults. **Submit** checks the baseline and all 7 faults. `SURVIVED` identifies a fault your tests missed. A baseline failure shows the test name and error. Empty suites do not pass.

## Offline pytest support

The supplied runner implements the same small pytest subset used by the OOP course: `pytest.raises` (with `match`), `pytest.mark.parametrize`, function and yield fixtures, `pytest.approx` for numbers, `pytest.fail`, `capsys` / `capfd` for Python output, `monkeypatch`, and `tmp_path`. Standard-library `unittest.mock.patch` also works. Use function-scoped fixtures and top-level test functions. Plugins, async tests, pytest classes with setup hooks, skip/xfail, and advanced fixture scopes are not supported.

The judge uses Python 3.11 and no network. This runner measures statement coverage with Python tracing and uses explicit faulty variants. It does **not** run pytest-cov or mutatest. Its acceptance result is specific to this course.

For an older saved tab, use **+** to open the current template. Keep the old tab intact.
