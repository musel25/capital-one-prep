## Approach

Each subclass checks only its own rule and passes the shared fields to
`super().__init__`, so the base class keeps the speed rule in one place. `Car.describe` and
`Ferry.travel_minutes` extend the base result instead of repeating its formula. Ceiling division
with integers avoids float rounding. Every method is O(1).

## Reference classes

```python
class Vehicle:
    def __init__(self, name: str, speed: int):
        if speed < 1:
            raise ValueError("speed must be at least 1 km/h")
        self.name = name
        self.speed = speed

    def travel_minutes(self, km: int) -> int:
        return -(-km * 60 // self.speed)

    def describe(self) -> str:
        return f"{self.name}: {self.speed} km/h"


class Bicycle(Vehicle):
    def __init__(self, name: str, speed: int = 15):
        if speed > 40:
            raise ValueError("a bicycle is at most 40 km/h")
        super().__init__(name, speed)


class Car(Vehicle):
    def __init__(self, name: str, speed: int, seats: int):
        if not 1 <= seats <= 9:
            raise ValueError("seats must be from 1 to 9")
        super().__init__(name, speed)
        self.seats = seats

    def describe(self) -> str:
        unit = "seat" if self.seats == 1 else "seats"
        return f"{super().describe()}, {self.seats} {unit}"


class Ferry(Vehicle):
    def __init__(self, name: str, speed: int, boarding: int = 20):
        if boarding < 0:
            raise ValueError("boarding time must not be negative")
        super().__init__(name, speed)
        self.boarding = boarding

    def travel_minutes(self, km: int) -> int:
        return self.boarding + super().travel_minutes(km)
```
