# 05. Alternative constructors

[Course list](/?course=python-oop) · Level 1: Classes and properties · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 01–04. Static methods and `__repr__`.

A class has one `__init__`, but you often get data in several formats. An
**alternative constructor** is a `@classmethod` that converts one format and then calls the class.
A class method receives the class as its first argument, named `cls` by convention.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    @classmethod
    def from_text(cls, text):          # "3,4"
        x, y = text.split(",")
        return cls(int(x), int(y))
```

Return `cls(...)`, not `Point(...)`. Then a subclass that calls `from_text` gets an instance of
the subclass. This is how `dict.fromkeys` and `datetime.fromisoformat` work.

`__eq__(self, other)` defines `==`. Return `NotImplemented` for a type that you do not support;
Python then tries the other operand and finally compares identity.

</details>

**Scenario:** A fitness app records workout durations. The phone sends seconds, the coach types
minutes, and imported files contain text like `1h 5m 30s`. All three must become the same
`Duration` type. A `Lap` is a special duration for one lap of a track.

Write the class `Duration`. The starter already contains `class Lap(Duration): pass`.
Keep it.

- `Duration(seconds)`: `seconds` is an integer. Negative raises `ValueError`. Store it in the
  attribute `seconds`.
- `from_minutes(minutes)`: **class method**. Return an instance of `cls` with `minutes * 60`
  seconds.
- `from_text(text)`: **class method**. Return an instance of `cls`. The text has one, two, or
  three parts, separated by **single spaces**. Each part is digits followed by one unit: `h`
  (hours), `m` (minutes), or `s` (seconds). The units appear in the order `h`, `m`, `s`, and each
  unit at most once. A part can be larger than one unit, for example `90m`. Any other text raises
  `ValueError`, including an empty string, a sign, a double space, or a repeated unit.
- `str(duration)`: write the duration with hours, minutes (0–59), and seconds (0–59). Show only
  parts that are not zero, in the order `h m s`, separated by spaces, for example `1h 5s`. Zero
  is `0s`.
- `a == b`: `True` when both are `Duration` instances (subclasses too) with the same `seconds`.
  For other types, return `NotImplemented`.

**Constraints:**

- Values are at most 10,000,000 seconds.
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

Python documentation: [1](https://docs.python.org/3.11/library/functions.html#classmethod), [2](https://docs.python.org/3.11/library/constants.html#NotImplemented)
