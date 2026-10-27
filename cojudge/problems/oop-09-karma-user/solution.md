## Approach

The receiver keeps a dictionary from giver to total points, so `karma` is a sum
and `fans` is a sort with the key `(-points, name)`. `thank` validates identity and points before
it changes either user, so a rejected thank-you leaves both unchanged. `__lt__` compares karma,
which makes `sorted(users)` order users from least to most karma.

## Reference classes

```python
class KarmaUser:
    def __init__(self, name: str):
        self.name = name
        self._received: dict[str, int] = {}
        self._given = 0

    def thank(self, other: "KarmaUser", points: int = 1) -> None:
        if other is self:
            raise ValueError("users cannot thank themselves")
        if isinstance(points, bool) or not isinstance(points, int) or not 1 <= points <= 3:
            raise ValueError("points must be an integer from 1 to 3")
        other._received[self.name] = other._received.get(self.name, 0) + points
        self._given += points

    @property
    def karma(self) -> int:
        return sum(self._received.values())

    @property
    def given(self) -> int:
        return self._given

    @property
    def fans(self) -> list[str]:
        return sorted(self._received, key=lambda name: (-self._received[name], name))

    def __str__(self) -> str:
        count = len(self._received)
        return f"{self.name}: {self.karma} karma from {count} {'fan' if count == 1 else 'fans'}"

    def __lt__(self, other: "KarmaUser") -> bool:
        return self.karma < other.karma
```
