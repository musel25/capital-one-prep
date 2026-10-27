# 12. Multiple inheritance and the MRO

[Course list](/?course=python-oop) · Level 3: Inheritance and composition · Hard · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 10–11. `super()` and class attributes.

A class can have several base classes: `class Alert(Shout, Tag, Trim)`. Python puts
all classes in one line, the **method resolution order** (MRO). See it with `Alert.__mro__`.
The MRO keeps each class before its bases, and keeps the order that you list the bases in.

`super()` does **not** mean "my base class". It means "the next class in the MRO of the
object's type". So in an `Alert` object, `super()` inside `Shout` calls `Tag`, although `Shout`
does not inherit from `Tag`. When every class calls `super()`, all of them run in MRO order. This
is **cooperative** multiple inheritance:

```python
class Base:
    def name(self): return "base"
class A(Base):
    def name(self): return "a>" + super().name()
class B(Base):
    def name(self): return "b>" + super().name()
class C(A, B): pass
C().name()   # "a>b>base"  (MRO: C, A, B, Base, object)
```

A class that does not call `super()` stops the chain: the classes after it never run.

</details>

**Scenario:** A monitoring system formats messages before it sends them. Small formatter
classes each do one thing: trim spaces, add a tag, or shout. Message types combine them with
multiple inheritance, so every new combination is one short class definition.

The starter gives the base class `Formatter`, where `format(text)` returns `text`.
Do not change it. Write these classes. Every `format` method must call `super().format(...)`
exactly once:

- `Trim(Formatter)`: pass `text.strip()` to the next `format` and return its result.
- `Shout(Formatter)`: take the result of the next `format(text)`, convert it to uppercase, and
  add `"!"`.
- `Tag(Formatter)`: class attribute `tag = "info"`. Return `"[<tag>] "` followed by the result of
  the next `format(text)`. Read the tag from `self.tag`.
- `Alert(Shout, Tag, Trim)`: class attribute `tag = "alert"`. No `format` method of its own.
- `Note(Tag, Trim)`: no new attributes or methods.

Example: `Alert().format("  disk full ")` runs `Shout`, `Tag`, `Trim`, then `Formatter`, and
returns `"[ALERT] DISK FULL!"`.

**Constraints:**

- Texts are ASCII.
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

Python documentation: [1](https://docs.python.org/3.11/library/functions.html#super), [2](https://docs.python.org/3.11/tutorial/classes.html#multiple-inheritance)
