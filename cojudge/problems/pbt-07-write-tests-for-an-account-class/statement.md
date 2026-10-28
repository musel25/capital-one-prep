In our third Test Bite you will write tests for (a reduced version of) the Account class Bob wrote for his Enriching Your Python Classes With Dunder (Magic, Special) Methods article. You can assume Accounts to be instantiated with integer amounts only.

For this version, write tests for the supplied code. Your tests must pass against the correct code, cover at least 90% of its executable statements, and detect every supplied faulty version. A fault is detected when at least one test fails. An empty test suite does not pass.

Import the target as `account`. The judge supplies it automatically.

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
