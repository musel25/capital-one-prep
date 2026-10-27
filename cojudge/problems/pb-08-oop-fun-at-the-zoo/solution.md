## Reference solution

```python
from itertools import count


class Animal:
    _sequence = count(10001)
    _animals = []

    def __init__(self, name):
        self.name = name.title()
        self.number = next(Animal._sequence)
        Animal._animals.append(self)

    def __str__(self):
        return f"{self.number}. {self.name}"

    @classmethod
    def zoo(cls):
        return "\n".join(str(animal) for animal in cls._animals)
```
