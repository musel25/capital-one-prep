# 08. Write your own data class

[Course list](/?course=python-oop) · Level 2: State and behavior · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 01–07. `__init__`, `__repr__`, and `__eq__`.

`@dataclass` writes the boring methods for you. You list the fields with type
annotations, and Python generates `__init__`, `__repr__`, and `__eq__`:

```python
from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int = 0
```

- `frozen=True` makes instances read-only: assignment raises `FrozenInstanceError`.
- `order=True` adds `<`, `<=`, `>`, `>=`. They compare the fields as a tuple, in definition order.
- `__post_init__(self)` runs after the generated `__init__`. Validate or convert fields there.
  In a frozen class, change a field with `object.__setattr__(self, "name", value)`.
- `dataclasses.replace(obj, x=5)` returns a copy with some fields changed. It calls `__init__`
  again, so `__post_init__` validates the copy too.

</details>

**Scenario:** A shop catalog keeps products as values: two products with the same fields are the
same product, and a product never changes after creation. A price change creates a new product.
Lists of products must sort by name, then price.

Write `Product` as a `@dataclass` with `frozen=True` and `order=True`.

- Fields, in this order: `name: str`, `price_cents: int`, `tags: tuple[str, ...] = ()`.
- `__post_init__`: an empty `name` or a negative `price_cents` raises `ValueError`. Convert
  `tags` to a tuple, because callers can pass a list.
- The generated methods give the rest:
  - `repr` is `Product(name='Pen', price_cents=150, tags=('office',))`.
  - `==` compares all fields. `<` compares `(name, price_cents, tags)`.
  - Assignment to any field raises `FrozenInstanceError`.
- `with_discount(percent)`: `percent` is an integer from 0 to 100; otherwise raise `ValueError`.
  Return a **new** product with price `price_cents * (100 - percent) // 100`. The original does
  not change.

**Constraints:**

- Names and tags are ASCII letters and spaces.
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

Python documentation: [1](https://docs.python.org/3.11/library/dataclasses.html)
