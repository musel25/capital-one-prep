# 07. Write tests for an account class

Write **tests**, not the implementation. [Original Pybites exercise](https://pybitesplatform.com/bites/write-tests-for-an-account-class/).

This is an offline recreation from the public description. The original code and template are premium and were not available. The API below belongs to this recreation.

## Contract

Account(owner, amount=0) stores a name and an integer initial amount. Reject non-integers including booleans. add_transaction accepts positive, negative, or zero integers. balance includes the initial amount and all transactions. len counts transactions. Indexing, slicing, and iteration expose transactions. str and repr use the exact formats in the supplied code. Compare Accounts by current balance, and return NotImplemented for unrelated types.

## Code to test

Import this module as `account`. The judge supplies it automatically.

```python
class Account:
    def __init__(self, owner, amount=0):
        if type(amount) is not int:
            raise TypeError('amount must be an integer')
        self.owner, self.amount = owner, amount
        self._transactions = []

    @property
    def balance(self):
        return self.amount + sum(self._transactions)

    def add_transaction(self, amount):
        if type(amount) is not int:
            raise TypeError('amount must be an integer')
        self._transactions.append(amount)

    def __len__(self):
        return len(self._transactions)

    def __getitem__(self, index):
        return self._transactions[index]

    def __str__(self):
        return f'Account of {self.owner} with starting amount: {self.amount}'

    def __repr__(self):
        return f'Account({self.owner!r}, {self.amount!r})'

    def __eq__(self, other):
        if not isinstance(other, Account):
            return NotImplemented
        return self.balance == other.balance

    def __lt__(self, other):
        if not isinstance(other, Account):
            return NotImplemented
        return self.balance < other.balance
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
