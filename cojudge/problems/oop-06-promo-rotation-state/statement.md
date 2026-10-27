# 06. No promo twice: keep state in a class

[Course list](/?course=python-oop) · Level 2: State and behavior · Easy · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Level 1. Properties and returning copies of lists.

An object remembers things between method calls. Create that state in `__init__`,
on `self`. Two common mistakes share state between objects:

- A **class attribute** such as `used = []` directly in the class body. All instances share that
  one list.
- A **mutable default argument** such as `def __init__(self, used=[])`. Python creates that list
  once, when it defines the function.

You can define your own exception: `class NoPromosLeft(Exception): pass`. A caller can then
catch exactly that error. `dict.fromkeys(items)` removes duplicates and keeps the first-seen
order, because dictionaries keep insertion order.

</details>

**Scenario:** An online shop gives each visitor a promo code from a campaign list. A visitor must
never get the same code twice. Each visitor's session has its own rotation object, so two
visitors never affect each other.

Write the exception `NoPromosLeft` (a subclass of `Exception`) and the class
`PromoRotation`.

- `PromoRotation(codes)`: `codes` is a list of strings. Keep the first occurrence of each code,
  in the given order. Use your own copy of the list.
- `draw()`: mark and return the first code in order that is not used yet. When every code is
  used, raise `NoPromosLeft`.
- `skip(code)`: mark `code` as used without returning it. An unknown code raises `ValueError`.
  A code that is already used does not change anything. Return `None`.
- `used`: read-only property. A new list of the used codes, in the order they were marked.
- `remaining`: read-only property. The number of codes that are not used.
- `reset()`: mark every code as not used. Return `None`.

Every rotation has its own state.

**Constraints:**

- At most 30 codes and 60 steps per test.
- Codes are non-empty strings.

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

Python documentation: [1](https://docs.python.org/3.11/tutorial/classes.html#class-and-instance-variables), [2](https://docs.python.org/3.11/tutorial/errors.html#user-defined-exceptions)
