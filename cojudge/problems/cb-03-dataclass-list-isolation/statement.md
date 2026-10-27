# 03. Trace state owned by an instance

[Course list](/?course=capital-one-codebase-practice) · Level 1 · Easy · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 01–02. The lesson introduces dataclasses and per-instance state.

The starter runs, but items placed in one box can appear in another box. Your objective is to trace which object owns a mutable list. Keep the dataclass model and repair its initialization behavior.

A dataclass can generate an initializer from annotated fields. A mutable field still needs a separate value for each instance. Use field(default_factory=list) to call list each time an instance is created. A factory must create a new value. A factory that returns one existing list still shares that list across instances. Then adding an item to one object changes another object. Dataclasses reject some direct mutable defaults, but a factory can hide the same defect. This task supplies a runnable faulty starter. Repair the shared state while keeping the dataclass model. The result for every box must depend only on actions addressed to that box.

</details>

**Input:** `data` has:
- `names`: distinct strings, one per box, in box order.
- `actions`: a list of `{"box": int, "item": string}`. `box` is a valid zero-based box index.

If `names` is empty, `actions` is empty too.

**Rules**
- Create one empty box per name.
- For each action, in order, append `item` to the selected box.

**Return** a list of `{"name": string, "items": [string]}`, one per box, in `names` order. Keep item order and duplicates.

The judge checks that the boxes are isolated. It does not check the dataclass syntax.

**What to fix:** The starter runs, but it has one intentional bug. The dataclass in the starter has a field factory that returns one shared list. Fix that defect.

- Repair the initialization of `Box.items`.
- Keep `Box` as a dataclass.
- Preserve names order, action order, empty boxes, and repeated items.
- Do not filter duplicates or rebuild the intended result from the actions at return time.
- The model itself must have independent state.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Create boxes named `left`, `middle`, and `right`. Apply actions `(box 2, "red")`, `(box 0, "blue")`, and `(box 2, "red")`. Required item lists are `["blue"]`, `[]`, and `["red", "red"]`. After each action, only one list may change. A different `Box` object is insufficient if its `items` field refers to the same list as another box.

### Read the existing code

Inspect `Box.items` and the factory used by that field. Follow the list comprehension in `solve` to the append operation. Draw three `Box` objects and arrows to their item lists. Ask when each list is created. Then inspect the output comprehension; it reports the state already stored in each box.

### Test before and after the change

First use two names and one action addressed only to the second box. Predict both lists before Run. Add three boxes with the middle box untouched, repeated equal items, no actions, and no names. If you save the starter locally, construct two `Box` instances and test that their item lists are distinct objects. Also call `solve` twice in one process to check that a later call starts empty. Separate judge checks may not expose state across calls.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “Using a dataclass factory guarantees a new list for every instance, regardless of what the factory returns.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py`. Trace the creation and use of `Box.items`. Cite the field declaration, the construction site, and the mutation site by file and line. Explain what must be true about list ownership. Do not suggest a factory expression or implement the repair. I will write the isolation regression.

### Technical completion checks

- Explain which lists must be distinct and why.
- Run a regression with an untouched box and a changed box.
- Review the field factory. A passing output check alone does not prove that the dataclass owns independent lists.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 04](/problems/cb-04-nested-copy-isolation).

Official documentation: [1](https://docs.python.org/3.11/library/dataclasses.html#default-factory-functions)
