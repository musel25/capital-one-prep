## Reference solution

```python
from functools import total_ordering


@total_ordering
class Account:

    def __init__(self, name, start_balance=0):
        self.name = name
        self.start_balance = start_balance
        self._transactions = []

    @property
    def balance(self):
        return self.start_balance + sum(self._transactions)

    def __len__(self):
        return len(self._transactions)

    def __eq__(self, other):
        return self.balance == other.balance

    def __lt__(self, other):
        return self.balance < other.balance

    def __getitem__(self, index):
        return self._transactions[index]

    def __iter__(self):
        return iter(self._transactions)

    def _check(self, amount):
        if type(amount) is not int:
            raise TypeError("amount must be an int")

    def __add__(self, amount):
        self._check(amount)
        self._transactions.append(amount)

    def __sub__(self, amount):
        self._check(amount)
        self._transactions.append(-amount)

    def __str__(self):
        return f"{self.name} account - balance: {self.balance}"
```
