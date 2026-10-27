## Approach

`PaymentMethod` declares `name` and `fee` abstract, so Python refuses to create the
base class or any subclass that misses one of them, such as `Draft`. `charge` is a template
method: it validates once and builds the receipt from the subclass's `name` and `fee`. `Wallet`
adds a precondition and a state change around `super().charge`, in an order that leaves the
balance unchanged when any check fails.

## Reference classes

```python
from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def fee(self, amount: int) -> int: ...

    def charge(self, amount: int) -> dict:
        if isinstance(amount, bool) or not isinstance(amount, int) or amount < 1:
            raise ValueError("amount must be a positive integer")
        fee = self.fee(amount)
        return {"method": self.name, "amount": amount, "fee": fee, "total": amount + fee}


class Card(PaymentMethod):
    name = "card"

    def fee(self, amount: int) -> int:
        return 30 + -(-amount * 29 // 1000)


class BankTransfer(PaymentMethod):
    name = "bank"

    def fee(self, amount: int) -> int:
        return 50


class Wallet(PaymentMethod):
    name = "wallet"

    def __init__(self, balance: int):
        if balance < 0:
            raise ValueError("balance must not be negative")
        self.balance = balance

    def fee(self, amount: int) -> int:
        return 0

    def charge(self, amount: int) -> dict:
        if amount > self.balance:
            raise ValueError("insufficient balance")
        receipt = super().charge(amount)
        self.balance -= amount
        return receipt


class Draft(PaymentMethod):
    """Unfinished: it has a name but no fee rule. Do not change this class."""
    name = "draft"
```
