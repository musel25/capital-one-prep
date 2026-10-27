# 13. Abstract base classes

[Course list](/?course=python-oop) · Level 3: Inheritance and composition · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 10–12. Subclasses and `super()`.

An **abstract base class** (ABC) defines what its subclasses must provide. It cannot
be instantiated itself:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> int: ...

    def describe(self) -> str:          # a normal method that uses the abstract one
        return f"area {self.area()}"
```

`Shape()` raises `TypeError`. A subclass that does not override **every** abstract method is
still abstract, and creating it also raises `TypeError`. This catches a missing method when the
object is created, not later when someone calls it.

An abstract property uses both decorators: `@property` above `@abstractmethod`. A subclass can
satisfy it with a plain class attribute, such as `name = "card"`.

`describe` above is a **template method**: the base class fixes the steps, and each subclass
fills in one step.

</details>

**Scenario:** A checkout service supports several payment methods. Every method must report its
name and fee, and every charge must produce the same receipt format. The team wants a new method
without a fee rule to fail as soon as it is created.

Write the abstract class `PaymentMethod` and three concrete subclasses. The starter
also has `Draft`, an unfinished payment method. Do not change `Draft`.

- `PaymentMethod(ABC)`:
  - `name`: abstract property.
  - `fee(amount)`: abstract method.
  - `charge(amount)`: a normal method. `amount` must be an `int` (not a `bool`) of at least 1;
    otherwise raise `ValueError`. Return the receipt
    `{"method": name, "amount": amount, "fee": fee, "total": amount + fee}`.
- `Card`: `name` is `"card"`. The fee is `30 + amount × 29 / 1000`, rounded **up**.
- `BankTransfer`: `name` is `"bank"`. The fee is always `50`.
- `Wallet(balance)`: `name` is `"wallet"`. A negative `balance` raises `ValueError`. Store it in
  `balance`. The fee is `0`. `charge(amount)` raises `ValueError` when `amount` is more than
  `balance`. Otherwise it uses the base `charge`, then subtracts `amount` from `balance`. A
  rejected charge does not change `balance`.

Creating `PaymentMethod` or `Draft` raises `TypeError`.

**Constraints:**

- Amounts in the tests are integers or booleans from -10 to 10,000,000.
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

Python documentation: [1](https://docs.python.org/3.11/library/abc.html)
