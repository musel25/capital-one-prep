## Approach

Both class methods convert their input and then call `cls(...)`, so `Lap.from_text`
returns a `Lap`, and validation stays in one place, `__init__`. The parser splits on single
spaces and tracks the last unit's position in `"hms"`, which rejects repeats and wrong order in
one comparison. `isdigit` alone also accepts other Unicode digits, so `isascii` is added.
`__eq__` returns `NotImplemented` for foreign types instead of `False`, which lets Python try the
other operand.

## Reference classes

```python
UNITS = {"h": 3600, "m": 60, "s": 1}


class Duration:
    def __init__(self, seconds: int):
        if seconds < 0:
            raise ValueError("a duration cannot be negative")
        self.seconds = seconds

    @classmethod
    def from_minutes(cls, minutes: int) -> "Duration":
        return cls(minutes * 60)

    @classmethod
    def from_text(cls, text: str) -> "Duration":
        total, last = 0, -1
        for part in text.split(" "):
            number, unit = part[:-1], part[-1:]
            if unit not in UNITS or not number.isdigit() or not number.isascii():
                raise ValueError(f"invalid part: {part!r}")
            position = "hms".index(unit)
            if position <= last:
                raise ValueError(f"unit out of order: {part!r}")
            last = position
            total += int(number) * UNITS[unit]
        return cls(total)

    def __str__(self) -> str:
        hours, rest = divmod(self.seconds, 3600)
        minutes, seconds = divmod(rest, 60)
        parts = [f"{n}{u}" for n, u in ((hours, "h"), (minutes, "m"), (seconds, "s")) if n]
        return " ".join(parts) or "0s"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented
        return self.seconds == other.seconds


class Lap(Duration):
    pass
```
