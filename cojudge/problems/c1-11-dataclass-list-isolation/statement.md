# 11. Fix shared dataclass items

[Course list](/?course=capital-one-engineering-50) · Level 2 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Classes, lists, and the first ten exercises.

A dataclass can generate an initializer from annotated fields. A mutable field still needs a separate value for each instance. Use field(default_factory=list) to call list each time an instance is created. A factory must create a new value. A factory that returns one existing list still shares that list across instances. Then adding an item to one object changes another object. Dataclasses reject some direct mutable defaults, but a factory can hide the same defect. This task supplies a runnable faulty starter. Repair the shared state while keeping the dataclass model. The result for every box must depend only on actions addressed to that box.

</details>

**Bug fix.** The dataclass in the starter has a field factory that returns one shared list. Fix that defect.

**Input:** `data` has:
- `names`: distinct strings, one per box, in box order.
- `actions`: a list of `{"box": int, "item": string}`. `box` is a valid zero-based box index.

If `names` is empty, `actions` is empty too.

**Rules**
- Create one empty box per name.
- For each action, in order, append `item` to the selected box.

**Return** a list of `{"name": string, "items": [string]}`, one per box, in `names` order. Keep item order and duplicates.

The judge checks that the boxes are isolated. It does not check the dataclass syntax.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/dataclasses.html#default-factory-functions)
