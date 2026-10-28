"""Bite: Subclassing: Vehicles in Motion (recreated tests and template)."""

SPEC = {
    "title": "Subclassing: Vehicles in Motion",
    "module": "vehicles",
    "template": '''class Vehicle:
    def __init__(self, brand: str, model: str, wheels: int) -> None:
        pass

    def description(self) -> str:
        pass


class Car(Vehicle):
    def __init__(self, brand: str, model: str, wheels: int, doors: int) -> None:
        pass

    def honk(self) -> str:
        pass


class Motorbike(Vehicle):
    def __init__(self, brand: str, model: str, wheels: int, engine_cc: int) -> None:
        pass

    def rev_engine(self) -> str:
        pass
''',
    "tests": '''import inspect

import pytest

from vehicles import Car, Motorbike, Vehicle


def test_vehicle():
    vehicle = Vehicle("Toyota", "Corolla", 4)
    assert vehicle.brand == "Toyota"
    assert vehicle.model == "Corolla"
    assert vehicle.wheels == 4
    assert vehicle.description() == "Toyota Corolla with 4 wheels"


def test_car():
    car = Car("Tesla", "Model 3", 4, 4)
    assert car.doors == 4
    assert car.brand == "Tesla"
    assert car.description() == "Tesla Model 3 with 4 wheels"
    assert car.honk() == "Beep beep!"


def test_motorbike():
    bike = Motorbike("Yamaha", "R3", 2, 321)
    assert bike.engine_cc == 321
    assert bike.wheels == 2
    assert bike.description() == "Yamaha R3 with 2 wheels"
    assert bike.rev_engine() == "Yamaha R3 with 2 wheels goes Vroom vroom!"


def test_keyword_arguments():
    bike = Motorbike(brand="Ducati", model="Monster", wheels=2, engine_cc=937)
    assert bike.rev_engine() == "Ducati Monster with 2 wheels goes Vroom vroom!"
    car = Car(brand="Fiat", model="500", wheels=4, doors=3)
    assert (car.model, car.doors) == ("500", 3)


def test_subclasses_inherit_from_vehicle():
    assert issubclass(Car, Vehicle)
    assert issubclass(Motorbike, Vehicle)
    assert isinstance(Car("A", "B", 4, 2), Vehicle)
    assert not hasattr(Car("A", "B", 4, 2), "rev_engine")
    assert not hasattr(Motorbike("A", "B", 2, 125), "honk")


@pytest.mark.parametrize("cls", [Car, Motorbike])
def test_subclass_constructor_uses_super(cls):
    assert "super()" in inspect.getsource(cls.__init__)


def test_rev_engine_reuses_description():
    """rev_engine must build on description(), so a change there shows up."""
    class LoudBike(Motorbike):
        def description(self):
            return "A loud bike"
    assert LoudBike("x", "y", 2, 50).rev_engine() == "A loud bike goes Vroom vroom!"
''',
    "reference": '''class Vehicle:
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
''',
}

SPEC["contract"] = (
    "brand and model are strings. wheels, doors and engine_cc are non-negative "
    "integers, excluding bool. Store the supplied values without normalization. "
    "Other types and negative counts are outside the contract; no validation is "
    "required for them. description returns '<brand> <model> with <wheels> wheels' "
    "from the current attributes. Car and Motorbike inherit Vehicle and use super() "
    "to initialize its attributes. honk returns 'Beep beep!'. rev_engine calls "
    "description and appends ' goes Vroom vroom!'. Instances keep separate attributes."
)
SPEC["tests"] += '''


def test_zero_and_unusual_counts_are_not_replaced_with_defaults():
    car = Car('Custom', 'Prototype', 6, 0)
    bike = Motorbike('Electric', 'Test', 0, 0)
    assert car.description() == 'Custom Prototype with 6 wheels'
    assert car.doors == 0
    assert bike.engine_cc == 0
    assert bike.rev_engine() == 'Electric Test with 0 wheels goes Vroom vroom!'


def test_description_uses_current_instance_attributes():
    first, second = Vehicle('A', 'B', 3), Vehicle('C', 'D', 5)
    first.brand, first.model, first.wheels = 'New', 'Model', 1
    assert first.description() == 'New Model with 1 wheels'
    assert second.description() == 'C D with 5 wheels'
'''
SPEC["mutations"] = [
    {"name": "hard-code four wheels", "old": "self.wheels = wheels", "new": "self.wheels = 4"},
    {"name": "replace zero doors with four", "old": "self.doors = doors", "new": "self.doors = doors or 4"},
    {"name": "replace zero engine capacity", "old": "self.engine_cc = engine_cc", "new": "self.engine_cc = engine_cc or 125"},
    {"name": "bypass overridden description", "old": "self.description()", "new": "Vehicle.description(self)"},
]
