## Reference solution

```python
class Account:

    def __init__(self):
        self._transactions = []

    @property
    def balance(self):
        return sum(self._transactions)

    def __add__(self, amount):
        self._transactions.append(amount)

    def __sub__(self, amount):
        self._transactions.append(-amount)

    def __enter__(self):
        self._snapshot = len(self._transactions)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.balance < 0:
            del self._transactions[self._snapshot:]
        return False
```
