# 09. Karma app: objects that interact

[Course list](/?course=python-oop) · Level 2: State and behavior · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 01–08. Properties, `__str__`, and instance state.

Objects often change **other** objects. In `alice.thank(bob)`, the method runs on
`alice`, but it updates `bob`'s state. Inside a class, a method may read and change the private
attributes of another instance of the same class.

Use `is` to test identity: `other is self` is `True` only for the same object, even when two
users have equal names.

`__lt__(self, other)` defines `<`. When it exists, `sorted(users)` works. To sort by several
keys, give `sorted` a key function that returns a tuple, for example
`key=lambda name: (-points[name], name)` for points high to low, then names A to Z.

</details>

**Scenario:** A team chat has a "thank you" button. A thank-you gives 1 to 3 karma points to a
colleague. Each profile shows the karma total and the top fans: the people who gave the most
points. Nobody can thank themselves.

Write the class `KarmaUser`.

- `KarmaUser(name)`: store `name`. A user starts with no karma.
- `thank(other, points=1)`: `other` receives `points` from this user. `points` is an integer
  from 1 to 3; otherwise raise `ValueError`. If `other` is this same object, raise `ValueError`.
  Return `None`.
- `karma`: read-only property. The total points this user received.
- `given`: read-only property. The total points this user gave.
- `fans`: read-only property. The names of everyone who thanked this user, once each. Sort by
  the total points they gave this user, high to low, then by name A to Z.
- `str(user)` returns `"<name>: <karma> karma from <n> fans"`. Use `fan` instead of `fans`
  when `n` is 1.
- `a < b` is `True` when `a` has less karma than `b`.

User names in one test are unique.

**Constraints:**

- At most 10 users and 60 steps per test.

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

Python documentation: [1](https://docs.python.org/3.11/reference/expressions.html#is-not), [2](https://docs.python.org/3.11/howto/sorting.html#key-functions)
