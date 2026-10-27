# 15. Subclass the dict built-in

[Course list](/?course=python-oop) · Level 4: Dunder methods and built-ins · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Level 3. Inheritance and `super()`.

You can inherit from a built-in type: `class Headers(dict):`. The object then **is**
a real dictionary: `isinstance(h, dict)` is `True`, and `json.dumps` accepts it.

There is a trap. The built-in `dict` is written in C, and its methods do **not** call each
other. If you override `__setitem__`, then `dict.__init__`, `dict.update`, `dict.get`, and
`dict.setdefault` still skip your code. You must override every method that you need, or route
them through your own code:

```python
class Headers(dict):
    def __init__(self, mapping=None):
        super().__init__()          # start empty
        if mapping is not None:
            self.update(mapping)    # your update, which uses your __setitem__
```

`collections.UserDict` avoids this trap because its methods call each other. In this exercise
you must use `dict` itself, so you learn where the trap is.

</details>

**Scenario:** An HTTP library stores response headers. Servers send `Content-Type`,
`content-type`, or `CONTENT-TYPE`, and all three mean the same header. Code that reads a header
must find it with any spelling.

Write `CaseInsensitiveDict`, a subclass of `dict`. All keys are strings. The
dictionary stores every key in **lowercase** and finds keys with any case.

- `CaseInsensitiveDict(mapping=None)`: start with the items of `mapping`, if given. When two keys
  differ only in case, the later value wins.
- `d[key] = value`, `d[key]`, and `key in d`: work with any case. A missing key raises `KeyError`.
- `get(key, default=None)`: like `dict.get`, with any case.
- `update(mapping)`: add or replace each item of `mapping` (a dictionary). Return `None`.
- `pop(key, default)`: remove the key and return its value. If the key is missing, return
  `default` when it is given; otherwise raise `KeyError`.

The driver shows the dictionary as a JSON object with the stored keys.

**Constraints:**

- Keys are ASCII strings. Values are JSON values.
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

Python documentation: [1](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict), [2](https://docs.python.org/3.11/library/collections.html#collections.UserDict)
