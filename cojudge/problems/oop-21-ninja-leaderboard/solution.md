## Approach

Each ninja maps to `(best, sequence)`. An accepted submission takes the next
sequence number, so "reached earlier" is a plain integer comparison, and an equal resubmission is
rejected before it can change that number. Every query sorts by `(-best, sequence)`: O(n log n)
per query and O(1) per submission. A heavy-traffic board would keep the order incrementally with
`bisect` or a balanced tree.

## Reference classes

```python
class Leaderboard:
    def __init__(self, size: int):
        if size < 1:
            raise ValueError("size must be at least 1")
        self.size = size
        self._best: dict[str, tuple[int, int]] = {}
        self._sequence = 0

    def submit(self, name: str, score: int) -> bool:
        current = self._best.get(name)
        if current is not None and score <= current[0]:
            return False
        self._sequence += 1
        self._best[name] = (score, self._sequence)
        return True

    def _ordered(self) -> list[str]:
        return sorted(self._best, key=lambda name: (-self._best[name][0], self._best[name][1]))

    def rank(self, name: str) -> int:
        if name not in self._best:
            raise KeyError(name)
        return self._ordered().index(name) + 1

    def top(self, n: int | None = None) -> list[tuple[str, int]]:
        limit = self.size if n is None else min(n, self.size)
        return [(name, self._best[name][0]) for name in self._ordered()[:limit]]

    def __len__(self) -> int:
        return len(self._best)

    def __contains__(self, name: object) -> bool:
        return name in self._best

    def __str__(self) -> str:
        return "\n".join(f"{place}. {name} {score}" for place, (name, score) in enumerate(self.top(), start=1))
```
