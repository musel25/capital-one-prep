## Approach

Each operator checks the operand type first and returns `NotImplemented` for
foreign types, so Python produces the standard `TypeError` (or `False` for `==`). Currency
mismatches are a supported type with a wrong value, so they raise `ValueError`. `total_ordering`
derives `<=`, `>`, and `>=` from `__lt__` and `__eq__`. `__rmul__ = __mul__` handles `2 * m`.
`__hash__` matches `__eq__`, so equal amounts work as dictionary keys.

## Reference classes

```python
from functools import total_ordering
import string


@total_ordering
class Money:
    def __init__(self, cents: int, currency: str):
        if isinstance(cents, bool) or not isinstance(cents, int):
            raise TypeError("cents must be an integer")
        if len(currency) != 3 or any(ch not in string.ascii_uppercase for ch in currency):
            raise ValueError(f"invalid currency: {currency!r}")
        self.cents = cents
        self.currency = currency

    def __repr__(self) -> str:
        return f"Money({self.cents}, {self.currency!r})"

    def __str__(self) -> str:
        units, rest = divmod(abs(self.cents), 100)
        sign = "-" if self.cents < 0 else ""
        return f"{self.currency} {sign}{units}.{rest:02d}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return (self.cents, self.currency) == (other.cents, other.currency)

    def __hash__(self) -> int:
        return hash((self.cents, self.currency))

    def _same_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(f"cannot mix {self.currency} and {other.currency}")

    def __lt__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return self.cents < other.cents

    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return Money(self.cents + other.cents, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            return NotImplemented
        self._same_currency(other)
        return Money(self.cents - other.cents, self.currency)

    def __mul__(self, factor: int) -> "Money":
        if isinstance(factor, bool) or not isinstance(factor, int):
            return NotImplemented
        return Money(self.cents * factor, self.currency)

    __rmul__ = __mul__

    def __bool__(self) -> bool:
        return self.cents != 0
```
