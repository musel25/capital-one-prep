# 16. Subclass the list built-in

[Course list](/?course=python-oop) · Level 4: Dunder methods and built-ins · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 15. Subclassing `dict` and its trap.

`list` has the same trap as `dict`: its methods do not call each other. `extend`,
`insert`, the constructor, and `lst[i] = x` all skip an overridden `append`. A validated list
must check every way in.

**All-or-nothing:** when one value in `extend([5, 200])` is invalid, the list must not keep the
`5`. Check every value first, then add them all. A half-finished change is a common bug in
real systems.

```python
def extend(self, values):
    values = [self._check(v) for v in values]   # may raise; nothing changed yet
    super().extend(values)
```

`list(values)` first is also important, because `values` can be an iterator that you can read
only once.

</details>

**Scenario:** A grading tool stores exam scores for one class. A score is a whole number from
0 to 100. The tool imports scores from files, so one bad value must not corrupt the list. The
list must still behave like a normal Python list for the rest of the code.

Write `Scores`, a subclass of `list`. A **valid score** is an `int` (not a `bool`) from
0 to 100. A value with the wrong type raises `TypeError`. An integer outside 0–100 raises
`ValueError`.

- `Scores(values=())`: validate every value. Invalid values raise as above.
- `append(value)`, `insert(index, value)`, and `scores[index] = value` (integer index): validate
  the value first, then behave like `list`.
- `extend(values)`: all-or-nothing. If any value is invalid, raise and add nothing.
- `average`: read-only property. `sum // len`. An empty list raises `ValueError`.
- `top(n)`: return a plain list of the `n` highest scores, highest first.

Other `list` behavior (indexing, `len`, `sorted`) works as usual. The driver shows the object as
a JSON list.

**Constraints:**

- At most 50 values and 40 steps per test.

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

Python documentation: [1](https://docs.python.org/3.11/library/stdtypes.html#lists), [2](https://docs.python.org/3.11/library/collections.html#collections.UserList)
