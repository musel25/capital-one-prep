"""Original exercise: composition instead of inheritance."""
from cojudge.oop.steps import call, case, check, error, get, new, obj, ref

SPEC = {
    "number": 14, "slug": "robot-composition", "title": "Composition or inheritance?",
    "difficulty": "Medium", "time": 30, "level": 3,
    "prerequisites": "Exercises 10–13. Inheritance and `super()`.",
    "learn": """Inheritance says "is a": a `Car` **is a** `Vehicle`. **Composition** says "has a": a
robot **has a** battery and **has a** motor. With composition, an object stores other objects in
attributes and asks them to do part of the work (it **delegates**).

```python
class Robot:
    def __init__(self, battery, motor):
        self.battery = battery      # a part, not a base class
        self.motor = motor
```

Composition is often the better choice:

- You can replace a part at run time (`robot.battery = spare`). A base class is fixed.
- The robot shows only the methods that make sense for a robot. If `Robot` inherited from
  `Battery`, it would also get `recharge` and `capacity`, which mix two ideas.
- Parts can be shared. Two objects can hold the **same** part object, so a change through one is
  visible through the other.""",
    "scenario": """A warehouse simulator models delivery robots. Each robot is built from a battery
and a motor. Batteries can be swapped at a charging station, and a test rig can power two robots
from one battery.""",
    "task": """Write `Battery`, `Motor`, and `Robot`. `Robot` must **not** inherit from `Battery` or
`Motor`.

- `Battery(capacity)`: `capacity` is an integer of at least 1; otherwise `ValueError`. The
  attribute `charge` starts at `capacity`.
  - `draw(units)`: take `min(units, charge)` from `charge` and return the amount taken. Negative
    `units` raises `ValueError`.
  - `recharge()`: set `charge` back to `capacity`. Return `None`.
  - `percent`: read-only property. `charge * 100 // capacity`.
- `Motor(cost_per_meter)`: an integer of at least 1; otherwise `ValueError`. `cost(meters)`
  returns `meters * cost_per_meter`.
- `Robot(battery, motor)`: stores both parts in the attributes `battery` and `motor`. `position`
  starts at 0.
  - `move(meters)`: negative raises `ValueError`. The robot moves as far as possible, up to
    `meters`: each meter costs `cost_per_meter` charge, and the robot never moves a part of a
    meter. Draw the cost from the battery, add the distance to `position`, and return it.
  - `swap_battery(battery)`: use the new battery and return the old one.""",
    "constraints": ["Values are at most 1,000,000.", "At most 50 steps per test."],
    "hints": ["The possible distance is `battery.charge // motor.cost_per_meter`.",
              "Delegate: the robot asks its battery to `draw` and its motor for the `cost`."],
    "starter": '''class Battery:
    def __init__(self, capacity: int):
        raise NotImplementedError

    def draw(self, units: int) -> int:
        raise NotImplementedError

    def recharge(self) -> None:
        raise NotImplementedError

    @property
    def percent(self) -> int:
        raise NotImplementedError


class Motor:
    def __init__(self, cost_per_meter: int):
        raise NotImplementedError

    def cost(self, meters: int) -> int:
        raise NotImplementedError


class Robot:
    def __init__(self, battery: Battery, motor: Motor):
        raise NotImplementedError

    def move(self, meters: int) -> int:
        raise NotImplementedError

    def swap_battery(self, battery: Battery) -> Battery:
        raise NotImplementedError
''',
    "reference": '''class Battery:
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
''',
    "facts": ["property Battery percent"],
    "java": '''static class Battery implements Obj { long capacity, charge; public String type() { return "Battery"; } }
static class Motor implements Obj { long cost; public String type() { return "Motor"; } }
static class Robot implements Obj { Battery battery; Motor motor; long position; public String type() { return "Robot"; } }
Object step(Map<String,Object> op) {
    String d = s(op.get("do"));
    Object t = target(op);
    if (d.equals("new")) {
        if (t.equals("Battery")) { Battery b = new Battery(); b.capacity = lng(arg(op, 0, "capacity", MISSING)); if (b.capacity < 1) throw err("ValueError"); b.charge = b.capacity; return b; }
        if (t.equals("Motor")) { Motor m = new Motor(); m.cost = lng(arg(op, 0, "cost_per_meter", MISSING)); if (m.cost < 1) throw err("ValueError"); return m; }
        Robot r = new Robot(); r.battery = (Battery) arg(op, 0, "battery", MISSING); r.motor = (Motor) arg(op, 1, "motor", MISSING); return r;
    }
    String name = op.containsKey("method") ? s(op.get("method")) : op.containsKey("attr") ? s(op.get("attr")) : "";
    if (t instanceof Battery) {
        Battery b = (Battery) t;
        if (d.equals("call") && name.equals("draw")) { long u = lng(args(op).get(0)); if (u < 0) throw err("ValueError"); long taken = Math.min(u, b.charge); b.charge -= taken; return taken; }
        if (d.equals("call") && name.equals("recharge")) { b.charge = b.capacity; return null; }
        if (d.equals("get") && name.equals("percent")) return b.charge * 100 / b.capacity;
        if (d.equals("get") && name.equals("charge")) return b.charge;
        if (d.equals("get") && name.equals("capacity")) return b.capacity;
    }
    if (t instanceof Motor) {
        Motor m = (Motor) t;
        if (d.equals("call") && name.equals("cost")) return lng(args(op).get(0)) * m.cost;
        if (d.equals("get") && name.equals("cost_per_meter")) return m.cost;
    }
    if (t instanceof Robot) {
        Robot r = (Robot) t;
        if (d.equals("call") && name.equals("move")) {
            long want = lng(args(op).get(0));
            if (want < 0) throw err("ValueError");
            long moved = Math.min(want, r.battery.charge / r.motor.cost);
            r.battery.charge -= moved * r.motor.cost; r.position += moved; return moved;
        }
        if (d.equals("call") && name.equals("swap_battery")) { Battery old = r.battery; r.battery = (Battery) args(op).get(0); return old; }
        if (d.equals("get") && name.equals("position")) return r.position;
        if (d.equals("get") && name.equals("battery")) return r.battery;
        if (d.equals("get") && name.equals("motor")) return r.motor;
    }
    throw err("AttributeError");
}
''',
    "approach": """`Robot` holds its parts and delegates: the battery knows its charge and the motor
knows its cost. The robot only combines them. Because the parts are separate objects, a swap is
one assignment, and two robots can share one battery object. Inheriting from `Battery` would give
`Robot` the wrong interface (`recharge`, `capacity`) and would make a battery swap impossible.""",
    "example_notes": [
        "Capacity 100 at 3 per meter: 100 // 3 = 33 whole meters. The robot moves 10, then only 23 more.",
        "Two robots share one battery object. The first robot uses 60 charge, so the second can move only 40.",
        "swap_battery returns the empty battery. The robot continues with the full one.",
    ],
    "cases": [
        case("moves until the battery is low",
             (new("Battery", 100, save="b"), obj("Battery")), (new("Motor", 3, save="m"), obj("Motor")),
             (new("Robot", ref("b"), ref("m"), save="r"), obj("Robot")), (call("r", "move", 10), 10),
             (call("r", "move", 50), 23), (get("r", "position"), 33), (get("b", "charge"), 1)),
        case("shared battery",
             (new("Battery", 100, save="b"), obj("Battery")), (new("Motor", 1, save="m"), obj("Motor")),
             (new("Robot", ref("b"), ref("m"), save="r1"), obj("Robot")), (new("Robot", ref("b"), ref("m"), save="r2"), obj("Robot")),
             (call("r1", "move", 60), 60), (call("r2", "move", 60), 40), (get("b", "percent"), 0)),
        case("swap battery",
             (new("Battery", 10, save="a"), obj("Battery")), (new("Battery", 50, save="b"), obj("Battery")),
             (new("Motor", 5, save="m"), obj("Motor")), (new("Robot", ref("a"), ref("m"), save="r"), obj("Robot")),
             (call("r", "move", 9), 2), (call("r", "swap_battery", ref("b"), save="old"), obj("Battery")),
             (get("old", "charge"), 0), (call("r", "move", 9), 9), (get("b", "charge"), 5)),
        case("not inherited",
             (check("subclass", "Robot", of="Battery"), False), (check("subclass", "Robot", of="Motor"), False),
             (check("property", "Battery", "percent"), True)),
        case("battery rules",
             (new("Battery", 0), error("ValueError")), (new("Battery", 8, save="b"), obj("Battery")),
             (call("b", "draw", 3), 3), (call("b", "draw", 10), 5), (call("b", "draw", -1), error("ValueError")),
             (get("b", "charge"), 0), (call("b", "recharge"), None), (get("b", "charge"), 8)),
        case("percent rounds down",
             (new("Battery", 3, save="b"), obj("Battery")), (call("b", "draw", 1), 1), (get("b", "percent"), 66),
             (call("b", "draw", 1), 1), (get("b", "percent"), 33)),
        case("motor rules",
             (new("Motor", 0), error("ValueError")), (new("Motor", 7, save="m"), obj("Motor")), (call("m", "cost", 3), 21),
             (call("m", "cost", 0), 0)),
        case("no partial meters",
             (new("Battery", 9, save="b"), obj("Battery")), (new("Motor", 4, save="m"), obj("Motor")),
             (new("Robot", ref("b"), ref("m"), save="r"), obj("Robot")), (call("r", "move", 5), 2), (call("r", "move", 1), 0),
             (get("b", "charge"), 1), (get("r", "position"), 2)),
        case("negative and zero moves",
             (new("Battery", 5, save="b"), obj("Battery")), (new("Motor", 1, save="m"), obj("Motor")),
             (new("Robot", ref("b"), ref("m"), save="r"), obj("Robot")), (call("r", "move", -1), error("ValueError")),
             (call("r", "move", 0), 0), (get("b", "charge"), 5)),
        case("recharge through the part",
             (new("Battery", 20, save="b"), obj("Battery")), (new("Motor", 2, save="m"), obj("Motor")),
             (new("Robot", ref("b"), ref("m"), save="r"), obj("Robot")), (call("r", "move", 100), 10),
             (call("b", "recharge"), None), (call("r", "move", 100), 10), (get("r", "position"), 20)),
        case("parts are reachable",
             (new("Battery", 20, save="b"), obj("Battery")), (new("Motor", 2, save="m"), obj("Motor")),
             (new("Robot", ref("b"), ref("m"), save="r"), obj("Robot")), (get("r", "battery"), obj("Battery")),
             (get("r", "motor"), obj("Motor")), (get("r", "position"), 0)),
        case("one motor for two robots with separate batteries",
             (new("Battery", 30, save="a"), obj("Battery")), (new("Battery", 30, save="b"), obj("Battery")),
             (new("Motor", 10, save="m"), obj("Motor")), (new("Robot", ref("a"), ref("m"), save="r1"), obj("Robot")),
             (new("Robot", battery=ref("b"), motor=ref("m"), save="r2"), obj("Robot")), (call("r1", "move", 5), 3),
             (call("r2", "move", 1), 1), (get("a", "charge"), 0), (get("b", "charge"), 20)),
    ],
    "generate": lambda rng: (
        [new("Battery", rng.randint(1, 200), save="a"), new("Battery", rng.randint(1, 200), save="b"),
         new("Motor", rng.randint(1, 9), save="m"), new("Robot", ref("a"), ref("m"), save="r"),
         new("Robot", ref(rng.choice("ab")), ref("m"), save="q")]
        + [rng.choice([call(rng.choice("rq"), "move", rng.randint(0, 40)), call(rng.choice("ab"), "recharge"),
                       get(rng.choice("ab"), "percent"), call("r", "swap_battery", ref(rng.choice("ab")), save="old"),
                       get(rng.choice("rq"), "position"), call(rng.choice("ab"), "draw", rng.randint(0, 50))])
           for _ in range(rng.randint(4, 14))]),
    "mutations": [
        {"name": "ignores the battery limit", "old": "moved = min(meters, self.battery.charge // self.motor.cost_per_meter)",
         "new": "moved = meters"},
        {"name": "swap returns the new battery", "old": "        old, self.battery = self.battery, battery\n        return old\n",
         "new": "        self.battery = battery\n        return battery\n"},
        {"name": "percent rounds up", "old": "self.charge * 100 // self.capacity", "new": "-(-self.charge * 100 // self.capacity)"},
    ],
    "sources": ["https://docs.python.org/3.11/tutorial/classes.html"],
}
