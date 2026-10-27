# 04. Color class with static methods

[Course list](/?course=python-oop) · Level 1: Classes and properties · Easy · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 01–03. Properties and `__repr__`.

A **static method** belongs to a class but does not receive `self` or `cls`. Mark it
with `@staticmethod`. Use it for a helper that is related to the class but does not need an
instance. You can call it on the class (`Color.hex_to_rgb("#ff0000")`) or on an instance.

```python
class Temperature:
    @staticmethod
    def c_to_f(celsius):
        return celsius * 9 // 5 + 32
```

Methods of the class can call the helper as `self.c_to_f(...)` or `Temperature.c_to_f(...)`.

Be careful with `int(text, 16)` for validation. It also accepts `"+f"`, `" ff"`, and `"f_f"`.
Check each character yourself when the format is strict.

</details>

**Scenario:** A design tool stores colors as hex codes such as `#ff8800`. Plugins need to convert
between hex codes and red/green/blue values without creating a color first. The tool also mixes
two colors for gradients.

Write the class `Color`.

- A **valid hex code** is a string of exactly 7 characters: `#` followed by 6 characters from
  `0-9`, `a-f`, or `A-F`.
- `Color.hex_to_rgb(code)`: **static method**. Return the tuple `(red, green, blue)` of integers.
  An invalid code raises `ValueError`.
- `Color.rgb_to_hex(red, green, blue)`: **static method**. Return `"#rrggbb"` in lowercase. Each
  value must be an `int` (not a `bool`) from 0 to 255; otherwise raise `ValueError`.
- `Color(code)`: an invalid code raises `ValueError`. Store the code in lowercase in the
  attribute `hex`.
- `rgb`: read-only property. Return `(red, green, blue)` for this color.
- `blend(other)`: return a **new** `Color`. Each component is `(mine + theirs) // 2`.
- `repr(color)` returns `Color('#rrggbb')`.

The driver shows tuples as JSON lists.

**Constraints:**

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

Python documentation: [1](https://docs.python.org/3.11/library/functions.html#staticmethod)
