# 21. Ninja rankings: a leaderboard class

[Course list](/?course=python-oop) · Level 5: Small projects · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Levels 1–4. Dunder methods `__len__`, `__contains__`, and `__str__`.

A leaderboard must be **fair** when scores are equal. A common rule: the player who
reached the score first ranks higher. To apply it, store a sequence number with each best score
and sort by `(-score, sequence)`.

```python
order = sorted(best, key=lambda name: (-best[name][0], best[name][1]))
```

Python's sort is **stable**, but stability alone is not enough here, because a dictionary keeps
the order in which a key was **first** inserted, not when its best score changed. The explicit
sequence number makes the rule independent of storage order.

`__len__` makes `len(board)` work, and `__contains__` makes `"Kai" in board` work. For a large
board, the `bisect` module keeps a list sorted while you insert; here a sort per query is fast
enough.

</details>

**Scenario:** A dojo app runs weekly training challenges. Each ninja can submit many times; only
their best score counts. The home screen shows the top of the board, and every ninja can look
up their own rank.

Write the class `Leaderboard`.

- `Leaderboard(size)`: `size` is the number of places shown by `top` and `str`. Below 1 raises
  `ValueError`.
- `submit(name, score)`: `score` is an integer. If `name` is new, or `score` is **higher** than
  their best, store it as their best and return `True`. Otherwise return `False` and change
  nothing.
- **Ranking order:** best score, high to low. For equal best scores, the ninja who **reached** that
  best score earlier ranks higher.
- `rank(name)`: the 1-based position among **all** ninjas. Unknown name: `KeyError`.
- `top(n=None)`: a list of `(name, score)` pairs for the first `n` places, but never more than
  `size`. With no `n`, use `size`. The driver shows pairs as lists.
- `len(board)`: the number of ninjas. `name in board`: `True` if the ninja submitted.
- `str(board)`: one line per place in `top()`, joined with `"\n"`, each `"<place>. <name>
  <score>"`. An empty board is `""`.

**Constraints:**

- Scores are from -1,000 to 1,000,000.
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

Python documentation: [1](https://docs.python.org/3.11/howto/sorting.html), [2](https://docs.python.org/3.11/library/bisect.html)
