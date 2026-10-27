# 14. Composition or inheritance?

[Course list](/?course=python-oop) · Level 3: Inheritance and composition · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 10–13. Inheritance and `super()`.

Inheritance says "is a": a `Car` **is a** `Vehicle`. **Composition** says "has a": a
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
  visible through the other.

</details>

**Scenario:** A warehouse simulator models delivery robots. Each robot is built from a battery
and a motor. Batteries can be swapped at a charging station, and a test rig can power two robots
from one battery.

Write `Battery`, `Motor`, and `Robot`. `Robot` must **not** inherit from `Battery` or
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
  - `swap_battery(battery)`: use the new battery and return the old one.

**Constraints:**

- Values are at most 1,000,000.
- At most 50 steps per test.

<details>
<summary><strong>How the tests work</strong></summary>

Each test is a list of steps. The supplied driver at the bottom of the editor runs
the steps on your classes, in order, and records one result per step:

- A step that raises records `{"error": "ExceptionName"}`, and the test continues.
- An object of a class records `{"object": "ClassName"}`. Tuples show as lists.

| Step `do` | What the driver runs |
| --- | --- |
| `new` | `cls(*args, **kwargs)` |
| `get` / `set` | `obj.attr` / `obj.attr = value` (records `null`) |
| `call` | `obj.method(*args, **kwargs)`; `obj` can also be a class name |
| `invoke` | `obj(*args)` |
| `op` | `left <op> right`, for example `a + b` or `a @ b` |
| `item` / `setitem` | `obj[key]` / `obj[key] = value` |
| `repr`, `str`, `len`, `bool`, `list`, `sorted` | the built-in function on `obj` |
| `with` | `with obj as name:` runs the inner `body` steps; `raise` raises that exception at the end of the block. Records `{"body": [...], "error": null or "ExceptionName"}` |
| `check` | the class structure, for example `"is": "property"` checks that `cls.attr` is a `property` |

`"save": "x"` stores a step's result under the name `x`. `{"ref": "x"}` inside a value means
that stored object. Copy an example's input into a custom test to debug it.

</details>

---

Select **Python**. Write your classes above the driver line. Do not edit the driver or the
`Solution.run` adapter. **Run** checks the three examples. **Submit** runs all 32 tests.
This is an original practice exercise.

Python documentation: [1](https://docs.python.org/3.11/tutorial/classes.html)
