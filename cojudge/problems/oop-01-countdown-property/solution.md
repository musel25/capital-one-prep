## Approach

`display` and `finished` are properties, so each read uses the current `seconds`.
`divmod` gives minutes and the remaining seconds, and `:02d` pads the seconds. Neither property
has a setter, so Python rejects assignment with `AttributeError`. Each operation is O(1).

## Reference classes

```python
class Countdown:
    def __init__(self, seconds: int):
        if seconds < 0:
            raise ValueError("seconds must not be negative")
        self.seconds = seconds

    @property
    def display(self) -> str:
        minutes, rest = divmod(self.seconds, 60)
        return f"{minutes}:{rest:02d}"

    @property
    def finished(self) -> bool:
        return self.seconds == 0

    def tick(self) -> int:
        if self.seconds > 0:
            self.seconds -= 1
        return self.seconds
```
