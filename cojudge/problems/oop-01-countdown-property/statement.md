# 01. Write a read-only property

[Course list](/?course=python-oop) · Level 1: Classes and properties · Easy · About 15 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Functions, f-strings, and a basic class with `__init__`.

A **property** is a method that you read like an attribute. Put `@property` above a
method, and `timer.display` calls it with no parentheses. Python computes the value each time you
read it, so the result is never out of date. If the class defines no setter, assignment to the
property raises `AttributeError`. That makes the value read-only.

```python
class Box:
    def __init__(self, width):
        self.width = width

    @property
    def area(self):
        return self.width * self.width
```

Use a property for a value that you calculate from other attributes. Do not calculate it once in
`__init__` and store it: a later change to `width` would leave a stale `area`.

</details>

**Scenario:** A kitchen timer app keeps the remaining time as a number of seconds. The screen
shows the time as minutes and seconds, for example `1:05`. The screen must always match the
current number of seconds.

Write the class `Countdown`.

- `Countdown(seconds)`: `seconds` is an integer. Store it in the public attribute `seconds`. If it
  is negative, raise `ValueError`.
- `display`: a read-only **property**. Return `"M:SS"`: whole minutes, a colon, and the remaining
  seconds as two digits. Minutes have no padding and can be more than 59. Examples: `0` → `"0:00"`,
  `65` → `"1:05"`, `3600` → `"60:00"`.
- `finished`: a read-only **property**. Return `True` when `seconds` is `0`.
- `tick()`: decrease `seconds` by 1, but never below 0. Return the new value of `seconds`.

Code can assign a new integer to `seconds` at any time. `display` and `finished` must then show
the new value. Assignment to `display` or `finished` raises `AttributeError`.

**Constraints:**

- `seconds` is an integer from -10 to 1,000,000.
- At most 60 steps per test.

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

Python documentation: [1](https://docs.python.org/3.11/library/functions.html#property)
