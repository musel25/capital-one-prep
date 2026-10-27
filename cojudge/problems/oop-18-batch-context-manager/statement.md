# 18. Write a context manager

[Course list](/?course=python-oop) · Level 4: Dunder methods and built-ins · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Level 3 and exercises 15–17. Properties and exceptions.

A `with` block calls two methods on an object:

```python
with batch as b:      # b = batch.__enter__()
    b.add(50)
# batch.__exit__(exc_type, exc_value, traceback) runs here, always
```

- `__enter__(self)` runs at the start. Its return value is bound by `as`. Often it returns `self`.
- `__exit__(self, exc_type, exc, tb)` runs at the end, **also when the block raises**. If the
  block ended normally, all three arguments are `None`. If the block raised, they describe the
  exception.
- If `__exit__` returns a true value, the exception is suppressed. Return `False` (or `None`) to
  let it continue. Suppressing errors by accident hides bugs.
- `__exit__` can raise its own exception, for example when a final check fails.

This is how files close themselves and how database transactions commit or roll back.

</details>

**Scenario:** A banking back office groups several balance changes into one batch. Either the
whole batch is applied, or none of it. If the code in the batch fails, or the result would make
the balance negative, nothing changes.

Write `Account` and `Batch`.

- `Account(balance)`: a negative `balance` raises `ValueError`. Store it in `balance`.
- `Batch(account)`: a batch can be used in **one** `with` block.
  - `__enter__`: return the batch. If the batch was already entered once, raise `RuntimeError`.
  - `add(amount)`: stage an amount. It is only allowed inside the `with` block; otherwise raise
    `RuntimeError`. `amount` must be a non-zero `int` (not a `bool`); otherwise `ValueError`. A
    rejected amount is not staged. Return `None`.
  - `pending`: read-only property. The sum of the staged amounts.
  - `committed`: read-only property. `True` after the batch was applied.
  - `__exit__`: the staged amounts are cleared in every case.
    - If the block raised, apply nothing and do **not** suppress the exception.
    - Otherwise, if `balance + pending` is negative, apply nothing and raise `ValueError`.
    - Otherwise add the sum to `account.balance` and mark the batch as committed.

The driver runs `with` blocks for you; see "How the tests work".

**Constraints:**

- Amounts are at most 10^9 in absolute value.
- At most 40 steps per test, including the steps inside blocks.

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

Python documentation: [1](https://docs.python.org/3.11/reference/datamodel.html#context-managers), [2](https://docs.python.org/3.11/reference/compound_stmts.html#the-with-statement)
