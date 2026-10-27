# 03. Write a score property with rules

[Course list](/?course=python-oop) · Level 1: Classes and properties · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 01–02. Properties and setters.

A setter is the single gate for a value. It can check the **type** and the
**range** of the new value and raise the right exception:

- `TypeError` when the value has the wrong type, for example a string instead of an integer.
- `ValueError` when the type is right but the value is not allowed, for example `-5`.

In Python, `True` and `False` are instances of `int`. Exclude them with an explicit check:
`isinstance(value, bool) or not isinstance(value, int)`.

When a property returns a list that the object owns, return a **copy** (`list(self._items)`).
Otherwise the caller can change the object's internal state without going through your rules.

</details>

**Scenario:** A quiz app shows each player's current score, their best score, and a score history
chart. The score comes from a network message, so it can have the wrong type. The history
chart must show exactly the scores that the app accepted.

Write the class `Player`.

- `Player(name)`: store `name`. The score starts at `0`.
- `score`: property with a setter. A new score must be an `int` that is not a `bool`; otherwise
  raise `TypeError`. A negative score raises `ValueError`. A rejected value changes nothing.
- `best`: read-only property. The highest score that was ever accepted (`0` at the start).
- `history`: read-only property. A **new list** of every accepted score in order, starting with
  the initial `0`. A change to the returned list must not change the player.
- `reset()`: set the score to `0` through the same rules. It is recorded in the history. `best`
  does not change. Return `None`.

The same score can be accepted twice; record it each time.

**Constraints:**

- Scores in the tests are from -100 to 10,000, or a wrong type.
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

Python documentation: [1](https://docs.python.org/3.11/library/functions.html#property), [2](https://docs.python.org/3.11/library/functions.html#isinstance)
