# 19. Matrix multiplication with @

[Course list](/?course=python-oop) · Level 4: Dunder methods and built-ins · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 17. Operator dunder methods and `NotImplemented`.

Python has an operator only for matrix multiplication: `a @ b` calls
`a.__matmul__(b)`. No built-in type uses it; libraries such as NumPy do. Your own class can too.

For an `m × n` matrix `A` and an `n × p` matrix `B`, the product `C = A @ B` is `m × p`. Each
entry is a row of `A` times a column of `B`:

```text
C[i][j] = A[i][0]*B[0][j] + A[i][1]*B[1][j] + ... + A[i][n-1]*B[n-1][j]
```

The inner sizes must match (`n`). `zip(*rows)` turns rows into columns, which makes the formula
short: `sum(a * b for a, b in zip(row, col))`.

A class that stores a list must protect it. Copy the rows when you receive them and when you
return them, so outside code cannot change the matrix.

</details>

**Scenario:** A small graphics engine transforms points with matrices: rotate, scale, and move.
Several transformations combine into one matrix by multiplication. The engine has no external
packages, so it needs its own `Matrix` type.

Write the class `Matrix`. Entries are integers.

- `Matrix(rows)`: `rows` is a non-empty list of non-empty lists, all with the same length;
  otherwise raise `ValueError`. Keep your own copy.
- `shape`: read-only property. `(row_count, column_count)`.
- `rows`: read-only property. A new list of new lists. A change to the result must not change the
  matrix.
- `Matrix.identity(n)`: **class method**. The `n × n` identity matrix (1 on the diagonal, 0
  elsewhere). `n` below 1 raises `ValueError`.
- `transpose()`: a new matrix with rows and columns exchanged.
- `a @ b`: a new matrix, the product. If the column count of `a` is not the row count of `b`,
  raise `ValueError`. A non-`Matrix` operand gives `TypeError` (return `NotImplemented`).
- `a == b`: `True` when the entries are equal. For a non-`Matrix`, return `NotImplemented`.
- `repr`: `Matrix([[1, 2], [3, 4]])`.

**Constraints:**

- At most 8 rows and 8 columns.
- Entries are from -1000 to 1000.
- At most 30 steps per test.

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

Python documentation: [1](https://docs.python.org/3.11/reference/datamodel.html#object.__matmul__), [2](https://peps.python.org/pep-0465/)
