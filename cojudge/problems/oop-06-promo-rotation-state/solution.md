## Approach

Both lists live on `self`, so each rotation is independent. `dict.fromkeys`
removes duplicates in order and also copies the input. `draw` scans in order and raises the
custom exception at the end. For n codes, `draw` is O(n²) with a list membership test; a set of
used codes next to the ordered list makes it O(n).

## Reference classes

```python
class NoPromosLeft(Exception):
    pass


class PromoRotation:
    def __init__(self, codes: list[str]):
        self._codes = list(dict.fromkeys(codes))
        self._used: list[str] = []

    def draw(self) -> str:
        for code in self._codes:
            if code not in self._used:
                self._used.append(code)
                return code
        raise NoPromosLeft("every code has been used")

    def skip(self, code: str) -> None:
        if code not in self._codes:
            raise ValueError(f"unknown code: {code!r}")
        if code not in self._used:
            self._used.append(code)

    @property
    def used(self) -> list[str]:
        return list(self._used)

    @property
    def remaining(self) -> int:
        return len(self._codes) - len(self._used)

    def reset(self) -> None:
        self._used.clear()
```
