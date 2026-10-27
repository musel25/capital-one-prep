## Approach

The setter checks the type, then the range, and only then changes three fields.
`reset` goes through the setter, so it is recorded like any other accepted score. `history`
returns a copy, so the caller cannot bypass the rules. Each operation is O(1) except `history`,
which is O(n) for the copy.

## Reference classes

```python
class Player:
    def __init__(self, name: str):
        self.name = name
        self._score = 0
        self._best = 0
        self._history = [0]

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("score must be an integer")
        if value < 0:
            raise ValueError("score must not be negative")
        self._score = value
        self._best = max(self._best, value)
        self._history.append(value)

    @property
    def best(self) -> int:
        return self._best

    @property
    def history(self) -> list[int]:
        return list(self._history)

    def reset(self) -> None:
        self.score = 0
```
