## Approach

Sound and legs are class attributes, so each species defines them once and
`speak` finds them through normal attribute lookup. An assignment on one animal creates an
instance attribute that shadows the class value for that animal only. Each zoo keeps its
dictionary and counter on `self`; a counter instead of `len(...) + 1` keeps numbers unique after
a release. Python dictionaries keep insertion order, which is number order here.

## Reference classes

```python
class Animal:
    sound = "..."
    legs = 0

    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} says {self.sound}"


class Lion(Animal):
    sound = "roar"
    legs = 4


class Parrot(Animal):
    sound = "squawk"
    legs = 2


class Snake(Animal):
    sound = "hiss"
    legs = 0


class Zoo:
    KINDS = {"lion": Lion, "parrot": Parrot, "snake": Snake}

    def __init__(self, name: str):
        self.name = name
        self._next = 1
        self._animals: dict[int, Animal] = {}

    def admit(self, kind: str, name: str) -> int:
        if kind not in self.KINDS:
            raise ValueError(f"unknown kind: {kind!r}")
        number = self._next
        self._next += 1
        self._animals[number] = self.KINDS[kind](name)
        return number

    def animal(self, number: int) -> Animal:
        return self._animals[number]

    def release(self, number: int) -> str:
        return self._animals.pop(number).name

    def roster(self) -> list[str]:
        return [f"#{number} {a.name} ({type(a).__name__})" for number, a in self._animals.items()]

    def total_legs(self) -> int:
        return sum(a.legs for a in self._animals.values())
```
