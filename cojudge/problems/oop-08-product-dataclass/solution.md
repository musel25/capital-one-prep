## Approach

The decorator generates `__init__`, `__repr__`, `__eq__`, the four ordering
methods, and `__hash__` (because the class is frozen and has `eq`). `__post_init__` validates and
converts `tags` with `object.__setattr__`, the documented way around `frozen`. `with_discount`
uses `replace`, which runs `__post_init__` again on the copy.

## Reference classes

```python
from dataclasses import dataclass, replace


@dataclass(frozen=True, order=True)
class Product:
    name: str
    price_cents: int
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must not be empty")
        if self.price_cents < 0:
            raise ValueError("price must not be negative")
        object.__setattr__(self, "tags", tuple(self.tags))

    def with_discount(self, percent: int) -> "Product":
        if not 0 <= percent <= 100:
            raise ValueError("percent must be from 0 to 100")
        return replace(self, price_cents=self.price_cents * (100 - percent) // 100)
```
