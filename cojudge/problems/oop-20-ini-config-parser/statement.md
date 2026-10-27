# 20. Complete an INI config parser class

[Course list](/?course=python-oop) · Level 5: Small projects · Hard · About 45 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Levels 1–4. Properties, `__contains__`, and exceptions.

A parser class reads text once, in `__init__`, and turns it into a clean data
structure. The other methods only answer questions about that structure. If the text is invalid,
raise in `__init__`: then no half-built object exists.

Parse line by line with a little **state**: the current section and the last key. Decide what
each line is in a fixed order, because some rules overlap. For example, an indented line is a
continuation even when it contains `=`.

```python
for line in text.split("\n"):
    stripped = line.strip()
    if not stripped or stripped[0] in "#;":
        continue            # blank or comment
    ...
```

`str.partition("=")` splits at the **first** `=` only, so a value can contain `=`. Python's
`configparser` module handles real INI files; here you write the rules yourself, so you control
every detail.

</details>

**Scenario:** A test runner reads its settings from a `tox.ini`-style file. A value can span
several indented lines, for example a list of dependencies. The runner must reject a broken file
with a clear error instead of running with wrong settings.

Write `IniConfig`. Split the text on `"\n"` and classify each line in this order:

1. **Blank or comment:** after stripping spaces and tabs, the line is empty or starts with `#`
   or `;`. Ignore it. It does not end a value.
2. **Continuation:** the line starts with a space or a tab. Append its stripped text to the value
   of the last key in the current section, separated by `"\n"`. If that value is empty, the text
   replaces it. Without a previous key in this section, raise `ValueError`.
3. **Section header:** the stripped line starts with `[` and ends with `]`. The name is the text
   between them, stripped. An empty or repeated name raises `ValueError`.
4. **Key line:** the line contains `=`. The key is the stripped text before the first `=`; the
   value is the stripped text after it. A key before any section, an empty key, or a repeated key
   in the same section raises `ValueError`.
5. Anything else raises `ValueError`.

Methods:

- `IniConfig(text)`: parse as above.
- `sections`: read-only property. The section names in file order.
- `keys(section)`: the keys of the section in file order. Unknown section: `KeyError`.
- `get(section, key, default=None)`: the value, or `default` if the section or key is missing.
- `get_list(section, key)`: split the value on newlines and commas, strip each item, drop empty
  items. Missing section or key: `KeyError`.
- `section in config`: `True` if the section exists.

**Constraints:**

- Text has at most 60 lines and contains no carriage returns.
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

Python documentation: [1](https://docs.python.org/3.11/library/stdtypes.html#str.partition), [2](https://docs.python.org/3.11/library/configparser.html)
