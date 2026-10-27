"""Original exercise: subclassing, overriding, and super()."""
from cojudge.oop.steps import call, case, check, error, get, new, obj, put

SPEC = {
    "number": 10, "slug": "vehicle-subclasses", "title": "Subclassing: vehicles in motion",
    "difficulty": "Easy", "time": 25, "level": 3,
    "prerequisites": "Level 2. Classes with `__init__` and methods.",
    "learn": """A **subclass** inherits every method of its base class: `class Car(Vehicle):`. It can
add new attributes and **override** methods. Call the base version with `super()`:

```python
class Car(Vehicle):
    def __init__(self, name, speed, seats):
        super().__init__(name, speed)   # the base class sets name and speed
        self.seats = seats

    def describe(self):
        return super().describe() + f", {self.seats} seats"
```

`super()` reuses the base logic instead of copying it. When the base class changes, the subclass
gets the change too. A subclass instance is also an instance of the base class:
`isinstance(car, Vehicle)` is `True`.

Integer ceiling division: `-(-a // b)` rounds `a / b` up without floats.""",
    "scenario": """A trip planner compares ways to travel: a bicycle, a car, or a ferry. All of them
move at a speed and estimate a travel time. Each kind adds its own rules: a bicycle has a speed
limit, a car has seats, and a ferry needs time to board.""",
    "task": """Write `Vehicle` and its subclasses `Bicycle`, `Car`, and `Ferry`.

- `Vehicle(name, speed)`: `speed` is an integer in km/h. Below 1 raises `ValueError`.
  - `travel_minutes(km)`: the minutes to travel `km` (an integer ≥ 0), rounded **up** to a whole
    minute: `km × 60 / speed`.
  - `describe()`: return `"<name>: <speed> km/h"`.
- `Bicycle(name, speed=15)`: a speed above 40 raises `ValueError`. Base rules also apply.
- `Car(name, speed, seats)`: `seats` is from 1 to 9; otherwise `ValueError`. Store `seats`.
  `describe()` adds `", <seats> seats"` to the base text, or `", 1 seat"` for one seat.
- `Ferry(name, speed, boarding=20)`: a negative `boarding` raises `ValueError`.
  `travel_minutes(km)` is `boarding` plus the base travel time.

Use `super()` in each subclass. A later change to `speed` must change the results.""",
    "constraints": ["Distances are from 0 to 10,000 km.", "At most 40 steps per test."],
    "hints": ["Call `super().__init__(name, speed)` so the base class validates `speed`.",
              "`Ferry.travel_minutes` can return `self.boarding + super().travel_minutes(km)`."],
    "starter": '''class Vehicle:
    def __init__(self, name: str, speed: int):
        raise NotImplementedError

    def travel_minutes(self, km: int) -> int:
        raise NotImplementedError

    def describe(self) -> str:
        raise NotImplementedError


class Bicycle(Vehicle):
    def __init__(self, name: str, speed: int = 15):
        raise NotImplementedError


class Car(Vehicle):
    def __init__(self, name: str, speed: int, seats: int):
        raise NotImplementedError


class Ferry(Vehicle):
    def __init__(self, name: str, speed: int, boarding: int = 20):
        raise NotImplementedError
''',
    "reference": '''class Vehicle:
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
''',
    "facts": ["subclass Bicycle Vehicle", "subclass Car Vehicle", "subclass Ferry Vehicle",
              "instance Car Vehicle", "instance Bicycle Vehicle", "instance Ferry Vehicle", "instance Car Car"],
    "java": '''static class V implements Obj {
    String kind, name; long speed, seats, boarding;
    public String type() { return kind; }
}
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    Object t = target(op);
    if (d.equals("new")) {
        V v = new V(); v.kind = (String) t; v.name = s(arg(op, 0, "name", MISSING));
        switch (v.kind) {
            case "Bicycle": v.speed = lng(arg(op, 1, "speed", 15L)); if (v.speed > 40) throw err("ValueError"); break;
            case "Car": v.speed = lng(arg(op, 1, "speed", MISSING)); v.seats = lng(arg(op, 2, "seats", MISSING));
                        if (v.seats < 1 || v.seats > 9) throw err("ValueError"); break;
            case "Ferry": v.speed = lng(arg(op, 1, "speed", MISSING)); v.boarding = lng(arg(op, 2, "boarding", 20L));
                          if (v.boarding < 0) throw err("ValueError"); break;
            default: v.speed = lng(arg(op, 1, "speed", MISSING));
        }
        if (v.speed < 1) throw err("ValueError");
        return v;
    }
    V v = (V) t;
    if (d.equals("call")) {
        String m = s(op.get("method"));
        if (m.equals("travel_minutes")) {
            long km = lng(args(op).get(0)), base = (km * 60 + v.speed - 1) / v.speed;
            return v.kind.equals("Ferry") ? v.boarding + base : base;
        }
        if (m.equals("describe")) {
            String text = v.name + ": " + v.speed + " km/h";
            return v.kind.equals("Car") ? text + ", " + v.seats + (v.seats == 1 ? " seat" : " seats") : text;
        }
    }
    if (d.equals("get")) {
        String a = s(op.get("attr"));
        if (a.equals("name")) return v.name;
        if (a.equals("speed")) return v.speed;
        if (a.equals("seats") && v.kind.equals("Car")) return v.seats;
        if (a.equals("boarding") && v.kind.equals("Ferry")) return v.boarding;
    }
    if (d.equals("set") && s(op.get("attr")).equals("speed")) { v.speed = lng(val(op.get("value"))); return null; }
    throw err("AttributeError");
}
''',
    "approach": """Each subclass checks only its own rule and passes the shared fields to
`super().__init__`, so the base class keeps the speed rule in one place. `Car.describe` and
`Ferry.travel_minutes` extend the base result instead of repeating its formula. Ceiling division
with integers avoids float rounding. Every method is O(1).""",
    "example_notes": [
        "The base class rounds up: 10 km at 60 km/h is exactly 10 minutes, 1 km at 7 km/h is 8.57, so 9.",
        "Car.describe extends the base text. The Ferry adds 20 minutes of boarding to the base time.",
        "A bicycle above 40 km/h is rejected by the subclass. Speed 0 is rejected by the base class through super().",
    ],
    "cases": [
        case("base vehicle",
             (new("Vehicle", "Bus", 60, save="v"), obj("Vehicle")), (call("v", "travel_minutes", 10), 10),
             (new("Vehicle", "Cart", 7, save="w"), obj("Vehicle")), (call("w", "travel_minutes", 1), 9),
             (call("v", "describe"), "Bus: 60 km/h")),
        case("subclasses extend the base",
             (new("Car", "Mini", 90, 4, save="c"), obj("Car")), (call("c", "describe"), "Mini: 90 km/h, 4 seats"),
             (new("Ferry", "Isla", 30, save="f"), obj("Ferry")), (call("f", "travel_minutes", 15), 50)),
        case("validation in subclass and base",
             (new("Bicycle", "Racer", 41), error("ValueError")), (new("Bicycle", "Slow", 0), error("ValueError")),
             (new("Bicycle", "City", save="b"), obj("Bicycle")), (get("b", "speed"), 15)),
        case("car seat rules and singular",
             (new("Car", "Kart", 40, 0), error("ValueError")), (new("Car", "Van", 100, 10), error("ValueError")),
             (new("Car", "Kart", 40, 1, save="c"), obj("Car")), (call("c", "describe"), "Kart: 40 km/h, 1 seat")),
        case("car speed still validated",
             (new("Car", "Broken", 0, 4), error("ValueError")), (new("Car", "Ok", 1, 4, save="c"), obj("Car")),
             (call("c", "travel_minutes", 1), 60)),
        case("ferry boarding options",
             (new("Ferry", "Quick", 60, 0, save="f"), obj("Ferry")), (call("f", "travel_minutes", 60), 60),
             (new("Ferry", "Slow", 20, boarding=45, save="g"), obj("Ferry")), (call("g", "travel_minutes", 0), 45),
             (new("Ferry", "Bad", 20, -1), error("ValueError"))),
        case("ferry describe is inherited",
             (new("Ferry", "Isla", 30, save="f"), obj("Ferry")), (call("f", "describe"), "Isla: 30 km/h"),
             (get("f", "boarding"), 20)),
        case("bicycle travel and boundary speed",
             (new("Bicycle", "Fast", 40, save="b"), obj("Bicycle")), (call("b", "travel_minutes", 10), 15),
             (call("b", "describe"), "Fast: 40 km/h"), (call("b", "travel_minutes", 0), 0)),
        case("speed changes later results",
             (new("Car", "Mini", 90, 4, save="c"), obj("Car")), (put("c", "speed", 45), None),
             (call("c", "travel_minutes", 3), 4), (call("c", "describe"), "Mini: 45 km/h, 4 seats")),
        case("rounding up",
             (new("Vehicle", "Train", 120, save="t"), obj("Vehicle")), (call("t", "travel_minutes", 1), 1),
             (call("t", "travel_minutes", 3), 2), (call("t", "travel_minutes", 10000), 5000)),
        case("instances of the base class",
             (new("Car", "Mini", 90, 4, save="c"), obj("Car")), (new("Vehicle", "Bus", 60, save="v"), obj("Vehicle")),
             (check("instance", "c", of="Vehicle"), True), (check("instance", "v", of="Car"), False)),
        case("structure",
             (check("subclass", "Bicycle", of="Vehicle"), True), (check("subclass", "Ferry", of="Vehicle"), True),
             (check("subclass", "Car", of="Ferry"), False), (new("Bicycle", name="Kid", speed=8, save="b"), obj("Bicycle")),
             (call("b", "travel_minutes", 2), 15)),
    ],
    "generate": lambda rng: (lambda kind: (
        [{"Vehicle": new("Vehicle", "V", rng.choice([0, 1, 13, 60, 99]), save="v"),
          "Bicycle": new("Bicycle", "B", rng.choice([10, 25, 40, 41]), save="v"),
          "Car": new("Car", "C", rng.choice([30, 77, 120]), rng.choice([0, 1, 2, 5, 9, 10]), save="v"),
          "Ferry": new("Ferry", "F", rng.choice([12, 25, 40]), rng.choice([0, 15, 20, -5]), save="v")}[kind]]
        + [rng.choice([call("v", "travel_minutes", rng.choice([0, 1, 7, 59, 61, 250, rng.randint(0, 10000)])),
                       call("v", "describe"), put("v", "speed", rng.randint(1, 150)), get("v", "speed")])
           for _ in range(rng.randint(3, 10))]))(rng.choice(["Vehicle", "Bicycle", "Car", "Ferry"])),
    "mutations": [
        {"name": "rounds down", "old": "-(-km * 60 // self.speed)", "new": "km * 60 // self.speed"},
        {"name": "ferry skips boarding", "old": "return self.boarding + super().travel_minutes(km)",
         "new": "return super().travel_minutes(km)"},
        {"name": "car always plural", "old": 'unit = "seat" if self.seats == 1 else "seats"', "new": 'unit = "seats"'},
        {"name": "bicycle default 20", "old": "def __init__(self, name: str, speed: int = 15):", "new": "def __init__(self, name: str, speed: int = 20):"},
    ],
    "sources": ["https://docs.python.org/3.11/tutorial/classes.html#inheritance",
                "https://docs.python.org/3.11/library/functions.html#super"],
}
