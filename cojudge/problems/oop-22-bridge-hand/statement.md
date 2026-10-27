# 22. Evaluate a bridge hand

[Course list](/?course=python-oop) · Level 5: Small projects · Hard · About 45 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Levels 1–4. Properties, `__str__`, and validation in `__init__`.

A domain class turns raw data into answers with names. Validate the raw data once in
`__init__`, keep it private, and expose each answer as a property. Each property is short
because it can use the others: `balanced` uses `shape`, and `shape` uses `lengths`.

**Bridge basics** for this exercise. A deck has 52 cards: 4 suits, spades `S`, hearts `H`,
diamonds `D`, and clubs `C`, with 13 ranks each, from low to high `2 3 4 5 6 7 8 9 T J Q K A`
(`T` is ten). A player gets 13 cards. Players evaluate a hand with simple counts:

- **High card points (HCP):** ace 4, king 3, queen 2, jack 1.
- **Shape:** the four suit lengths, sorted from long to short, such as `5-4-3-1`.
- **Losing trick count:** for each suit, look at its `min(length, 3)` highest cards. Count one
  loser for each of those positions that is not filled by the matching honor, A, K, Q in order.

`"23456789TJQKA".index(rank)` gives a rank's strength for sorting.

</details>

**Scenario:** A bridge training app shows a hand and asks the student to evaluate it. The app
then shows the correct counts and a suggested opening bid from a simplified practice system, so
the student can check their work.

Write the class `Hand`. A card is a two-character string: a suit (`S`, `H`, `D`,
`C`) and a rank (`2`–`9`, `T`, `J`, `Q`, `K`, `A`), all uppercase.

- `Hand(cards)`: a list of exactly 13 different valid cards; otherwise raise `ValueError`.
- `hcp`: property. High card points (A 4, K 3, Q 2, J 1).
- `lengths`: property. `{"S": n, "H": n, "D": n, "C": n}`.
- `shape`: property. The four lengths from long to short, joined with `-`, such as `"5-4-3-1"`.
- `balanced`: property. `True` when the shape is `4-3-3-3`, `4-4-3-2`, or `5-3-3-2`.
- `losers`: property. The losing trick count: for each suit with `n` cards, `min(n, 3)` minus the
  number of honors from `"AKQ"[:min(n, 3)]` in that suit. Add the four suits.
  Examples: void 0, `A` 0, `K` 1, `KQ` 1, `Qx` 2, `AKx` 1, `KQJ` 1, `xxxx` 3.
- `str(hand)`: `"S: <ranks> | H: <ranks> | D: <ranks> | C: <ranks>"`, ranks high to low with no
  spaces, `-` for a void. Example: `S: AK72 | H: QJ5 | D: A98 | C: K43`.
- `opening()`: the first rule that matches:
  1. HCP ≥ 22: `"2C"`.
  2. Balanced and HCP 15–17: `"1NT"`.
  3. Balanced and HCP 20–21: `"2NT"`.
  4. HCP ≥ 12: `"1"` + the longest suit. For equal lengths, use the first suit in `S H D C`.
  5. Otherwise `"pass"`.

The card order in the input does not matter.

**Constraints:**

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

Python documentation: [1](https://docs.python.org/3.11/library/functions.html#property), [2](https://docs.python.org/3.11/library/functions.html#max)
