# 07. Make an instance callable

[Course list](/?course=python-oop) · Level 2: State and behavior · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 06. Instance state.

`__call__` lets you call an object like a function: `throttle(12)` runs
`throttle.__call__(12)`. A callable object is useful when a "function" must remember something
between calls, and you also want to inspect that memory or configure it.

```python
class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count
```

`callable(obj)` is `True` when the object has `__call__`. A `collections.deque` is a good
container for a sliding window: append new items on the right, and `popleft()` old items.

</details>

**Scenario:** An API gateway limits each client to a number of requests in a time window, for
example 3 requests in any 10 seconds. The gateway calls the client's throttle object with the
current time for each request. The object answers `True` (allow) or `False` (reject).

Write the class `Throttle`.

- `Throttle(limit, window)`: both are integers. A value below 1 raises `ValueError`.
- `throttle(now)`: `now` is an integer time in seconds. Times never decrease from one call to the
  next. The window for this call holds the times `t` of accepted calls with
  `now - window < t <= now`. If the window holds fewer than `limit` calls, accept: record `now`
  and return `True`. Otherwise return `False`. A rejected call is **not** recorded.
- `accepted` and `rejected`: read-only properties. The number of calls that returned `True` and
  `False`.
- `repr(throttle)` returns `Throttle(limit=3, window=10)` with the real values.

**Constraints:**

- Times are from 0 to 1,000,000.
- At most 80 steps per test.

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

Python documentation: [1](https://docs.python.org/3.11/reference/datamodel.html#object.__call__), [2](https://docs.python.org/3.11/library/collections.html#collections.deque)
