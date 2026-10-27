## Reference solution

```python
from statistics import mean, median


class IntList(list):

    @staticmethod
    def _validate(values):
        values = list(values)
        for value in values:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"only numbers allowed, not {type(value).__name__}")
        return values

    @property
    def mean(self):
        return mean(self)

    @property
    def median(self):
        return median(self)

    def append(self, value):
        if isinstance(value, list):
            super().extend(self._validate(value))
        else:
            super().append(*self._validate([value]))

    def __add__(self, other):
        return IntList(list(self) + self._validate(other))

    def __iadd__(self, other):
        return super().__iadd__(self._validate(other))
```
