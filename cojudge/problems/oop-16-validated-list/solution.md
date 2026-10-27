## Approach

One `_check` helper holds the rule, and every entry point calls it: the
constructor (through `extend`), `append`, `insert`, and item assignment. `extend` builds the
validated list before it changes anything, so an invalid value leaves the list unchanged.
`average` uses integer division. `top` sorts a copy in O(n log n).

## Reference classes

```python
class Scores(list):
    def __init__(self, values=()):
        super().__init__()
        self.extend(values)

    @staticmethod
    def _check(value: int) -> int:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"a score must be an integer, not {type(value).__name__}")
        if not 0 <= value <= 100:
            raise ValueError(f"a score must be from 0 to 100, not {value}")
        return value

    def append(self, value: int) -> None:
        super().append(self._check(value))

    def extend(self, values) -> None:
        values = [self._check(v) for v in values]
        super().extend(values)

    def insert(self, index: int, value: int) -> None:
        super().insert(index, self._check(value))

    def __setitem__(self, index: int, value: int) -> None:
        super().__setitem__(index, self._check(value))

    @property
    def average(self) -> int:
        if not self:
            raise ValueError("no scores")
        return sum(self) // len(self)

    def top(self, n: int) -> list[int]:
        return sorted(self, reverse=True)[:n]
```
