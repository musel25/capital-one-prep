# 10. Subclassing: vehicles in motion

[Course list](/?course=python-oop) · Level 3: Inheritance and composition · Easy · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Level 2. Classes with `__init__` and methods.

A **subclass** inherits every method of its base class: `class Car(Vehicle):`. It can
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

Integer ceiling division: `-(-a // b)` rounds `a / b` up without floats.

</details>

**Scenario:** A trip planner compares ways to travel: a bicycle, a car, or a ferry. All of them
move at a speed and estimate a travel time. Each kind adds its own rules: a bicycle has a speed
limit, a car has seats, and a ferry needs time to board.

Write `Vehicle` and its subclasses `Bicycle`, `Car`, and `Ferry`.

- `Vehicle(name, speed)`: `speed` is an integer in km/h. Below 1 raises `ValueError`.
  - `travel_minutes(km)`: the minutes to travel `km` (an integer ≥ 0), rounded **up** to a whole
    minute: `km × 60 / speed`.
  - `describe()`: return `"<name>: <speed> km/h"`.
- `Bicycle(name, speed=15)`: a speed above 40 raises `ValueError`. Base rules also apply.
- `Car(name, speed, seats)`: `seats` is from 1 to 9; otherwise `ValueError`. Store `seats`.
  `describe()` adds `", <seats> seats"` to the base text, or `", 1 seat"` for one seat.
- `Ferry(name, speed, boarding=20)`: a negative `boarding` raises `ValueError`.
  `travel_minutes(km)` is `boarding` plus the base travel time.

Use `super()` in each subclass. A later change to `speed` must change the results.

**Constraints:**

- Distances are from 0 to 10,000 km.
- At most 40 steps per test.

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

Python documentation: [1](https://docs.python.org/3.11/tutorial/classes.html#inheritance), [2](https://docs.python.org/3.11/library/functions.html#super)
