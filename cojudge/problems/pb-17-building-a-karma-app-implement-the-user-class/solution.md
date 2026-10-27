## Reference solution

```python
from collections import namedtuple

Transaction = namedtuple('Transaction', 'giver points')


class User:

    def __init__(self, name):
        self.name = name
        self._transactions = []

    @property
    def karma(self):
        return sum(self.points)

    @property
    def points(self):
        return [t.points for t in self._transactions]

    @property
    def fans(self):
        return len({t.giver.name for t in self._transactions})

    def __add__(self, transaction):
        self._transactions.append(transaction)
        return self

    def __lt__(self, other):
        return self.karma < other.karma

    def __str__(self):
        fans = self.fans
        return f"{self.name} has a karma of {self.karma} and {fans} {'fan' if fans == 1 else 'fans'}"
```
