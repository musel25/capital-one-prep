# 17. Enrich a class with dunder methods

[Course list](/?course=python-oop) · Level 4: Dunder methods and built-ins · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 05 and 15–16. `__eq__`, `__repr__`, and `NotImplemented`.

Python operators call **dunder methods**: `a + b` calls `a.__add__(b)`, `a < b` calls
`a.__lt__(b)`, and `bool(a)` calls `a.__bool__()`. Implement them, and your objects work with
normal Python syntax.

When a method gets an operand that it does not support, it must **return** `NotImplemented` (it
must not raise). Python then tries the reflected method on the other operand, for example
`b.__radd__(a)`. If both return `NotImplemented`, Python raises `TypeError`, or for `==` falls
back to identity. `__rmul__` makes `2 * price` work, not only `price * 2`.

`functools.total_ordering` writes `<=`, `>`, and `>=` for you when you define `__eq__` and
`__lt__`. If you define `__eq__`, define `__hash__` too, or instances are unhashable.

Raise `ValueError` for a supported type with a bad value, such as two different currencies.

</details>

**Scenario:** An invoicing service adds and compares amounts of money. Amounts are whole cents,
never floats. Adding euros to dollars is a bug that must fail loudly, not silently produce a
wrong total.

Write the class `Money`.

- `Money(cents, currency)`: `cents` must be an `int` (not a `bool`); otherwise raise `TypeError`.
  `currency` must be three uppercase ASCII letters; otherwise raise `ValueError`.
- `repr`: `Money(1250, 'EUR')`. `str`: `EUR 12.50`. Negative amounts: `EUR -0.05`.
- `a == b`: `True` for the same cents and currency. For a non-`Money` operand, return
  `NotImplemented` (so `money == 5` is `False`). Make `Money` hashable.
- `a < b`, `<=`, `>`, `>=`: compare cents. Different currencies raise `ValueError`. A non-`Money`
  operand gives `TypeError` (return `NotImplemented`).
- `a + b` and `a - b`: a new `Money`. Different currencies raise `ValueError`. A non-`Money`
  operand gives `TypeError`.
- `money * n` and `n * money`: `n` is an `int` (not a `bool`). Other types give `TypeError`.
- `bool(money)` is `False` only for zero cents.

**Constraints:**

- Amounts are at most 10^12 cents.
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

Python documentation: [1](https://docs.python.org/3.11/reference/datamodel.html#emulating-numeric-types), [2](https://docs.python.org/3.11/library/functools.html#functools.total_ordering)
