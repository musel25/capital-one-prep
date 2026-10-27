## Approach

The batch is a small state machine: new, open, then committed or discarded.
`__exit__` always clears the staged amounts first, then chooses one outcome. With an exception
in the block it discards and returns `False`, so the original exception continues. Without one,
it checks the final balance once and either raises or applies the total in a single assignment,
so the account never shows a partial batch.

## Reference classes

```python
class Account:
    def __init__(self, balance: int):
        if balance < 0:
            raise ValueError("balance must not be negative")
        self.balance = balance


class Batch:
    def __init__(self, account: Account):
        self.account = account
        self._staged: list[int] = []
        self._state = "new"

    def __enter__(self) -> "Batch":
        if self._state != "new":
            raise RuntimeError("a batch can be used only once")
        self._state = "open"
        return self

    def add(self, amount: int) -> None:
        if self._state != "open":
            raise RuntimeError("add is only allowed inside the with block")
        if isinstance(amount, bool) or not isinstance(amount, int) or amount == 0:
            raise ValueError("amount must be a non-zero integer")
        self._staged.append(amount)

    @property
    def pending(self) -> int:
        return sum(self._staged)

    @property
    def committed(self) -> bool:
        return self._state == "committed"

    def __exit__(self, exc_type, exc, tb) -> bool:
        total, self._staged = sum(self._staged), []
        if exc_type is not None:
            self._state = "discarded"
            return False
        if self.account.balance + total < 0:
            self._state = "discarded"
            raise ValueError("the batch would make the balance negative")
        self.account.balance += total
        self._state = "committed"
        return False
```
