## Reference solution

```python
class Vehicle:
    def __init__(self, brand: str, model: str, wheels: int) -> None:
        self.brand = brand
        self.model = model
        self.wheels = wheels

    def description(self) -> str:
        return f"{self.brand} {self.model} with {self.wheels} wheels"


class Car(Vehicle):
    def __init__(self, brand: str, model: str, wheels: int, doors: int) -> None:
        super().__init__(brand, model, wheels)
        self.doors = doors

    def honk(self) -> str:
        return "Beep beep!"


class Motorbike(Vehicle):
    def __init__(self, brand: str, model: str, wheels: int, engine_cc: int) -> None:
        super().__init__(brand, model, wheels)
        self.engine_cc = engine_cc

    def rev_engine(self) -> str:
        return f"{self.description()} goes Vroom vroom!"
```
