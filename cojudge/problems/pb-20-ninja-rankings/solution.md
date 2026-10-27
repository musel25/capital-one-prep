## Reference solution

```python
from functools import total_ordering


@total_ordering
class Ninja:
    def __init__(self, name, bites):
        self.name = name
        self.bites = bites

    def __eq__(self, other):
        return self.bites == other.bites

    def __lt__(self, other):
        return self.bites < other.bites

    def __str__(self):
        return f"[{self.bites}] {self.name}"


class Rankings:
    def __init__(self):
        self._ninjas = []

    def add(self, ninja):
        self._ninjas.append(ninja)
        self._ninjas.sort(reverse=True)

    def dump(self):
        return self._ninjas.pop()

    def highest(self, count=1):
        return self._ninjas[:count]

    def lowest(self, count=1):
        return self._ninjas[::-1][:count]

    def __len__(self):
        return len(self._ninjas)

    def pair_up(self, count=3):
        return list(zip(self.highest(count), self.lowest(count)))
```
