# 02. Member class: properties, repr and str

[Course list](/?course=python-oop) · Level 1: Classes and properties · Easy · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 01. Read-only properties.

A property can also have a **setter**. Write `@email.setter` above a second method
with the same name. Assignment `member.email = "x"` then calls it, so you can validate the value
before you store it. Store the real value in a "private" attribute such as `self._email`. If
`__init__` assigns `self.email = email`, the constructor uses the same validation.

Two dunder methods control how an object looks as text:

- `__repr__` is for developers. A good repr looks like the code that creates the object, for
  example `Member('Ann', 'Lee', 'ann@mail.io')`. Use `!r` in an f-string to quote a value:
  `f"{self.first!r}"`.
- `__str__` is for users. `str(obj)` and `print(obj)` use it.

</details>

**Scenario:** A club website stores its members. The admin page shows `str(member)`. Logs and the
debugger show `repr(member)`. A typo in an email address must be rejected when it is entered,
not later when the club sends a message.

Write the class `Member`.

- `Member(first, last, email)`: store `first` and `last` in public attributes. Set the email
  through the `email` setter, so an invalid email raises `ValueError`.
- `full_name`: read-only property. Return `"<first> <last>"`.
- `handle`: read-only property. Return the first letter of `first` followed by `last`, all in
  lowercase. Example: `Ann Lee` → `"alee"`.
- `email`: property with a setter. An email is valid when all of these are true:
  - It contains exactly one `@`.
  - The part before `@` is not empty.
  - The part after `@` contains a `.`, and does not start or end with `.`.

  An invalid value raises `ValueError` and keeps the old email.
- `repr(member)` returns `Member('<first>', '<last>', '<email>')`.
- `str(member)` returns `<first> <last> <<email>>`, for example `Ann Lee <ann@mail.io>`.

A change to `first` or `last` must show in every later result.

**Constraints:**

- Names contain letters only and are not empty.
- Emails contain no spaces, quotes, or backslashes.
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

Python documentation: [1](https://docs.python.org/3.11/library/functions.html#property), [2](https://docs.python.org/3.11/reference/datamodel.html#object.__repr__)
