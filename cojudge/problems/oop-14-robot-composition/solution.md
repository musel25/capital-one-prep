## Approach

`Robot` holds its parts and delegates: the battery knows its charge and the motor
knows its cost. The robot only combines them. Because the parts are separate objects, a swap is
one assignment, and two robots can share one battery object. Inheriting from `Battery` would give
`Robot` the wrong interface (`recharge`, `capacity`) and would make a battery swap impossible.

## Reference classes

```python
class Battery:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self.charge = capacity

    def draw(self, units: int) -> int:
        if units < 0:
            raise ValueError("units must not be negative")
        taken = min(units, self.charge)
        self.charge -= taken
        return taken

    def recharge(self) -> None:
        self.charge = self.capacity

    @property
    def percent(self) -> int:
        return self.charge * 100 // self.capacity


class Motor:
    def __init__(self, cost_per_meter: int):
        if cost_per_meter < 1:
            raise ValueError("cost per meter must be at least 1")
        self.cost_per_meter = cost_per_meter

    def cost(self, meters: int) -> int:
        return meters * self.cost_per_meter


class Robot:
    def __init__(self, battery: Battery, motor: Motor):
        self.battery = battery
        self.motor = motor
        self.position = 0

    def move(self, meters: int) -> int:
        if meters < 0:
            raise ValueError("meters must not be negative")
        moved = min(meters, self.battery.charge // self.motor.cost_per_meter)
        self.battery.draw(self.motor.cost(moved))
        self.position += moved
        return moved

    def swap_battery(self, battery: Battery) -> Battery:
        old, self.battery = self.battery, battery
        return old
```
