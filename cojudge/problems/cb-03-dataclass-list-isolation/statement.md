# 03. Trace state owned by an instance

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 1 · Easy · About 30 minutes**

**Before this problem:** Exercises 01–02. The lesson introduces dataclasses and per-instance state.

## Learn first

The starter runs, but items placed in one box can appear in another box. Your objective is to trace which object owns a mutable list. Keep the dataclass model and repair its initialization behavior.

A dataclass can generate an initializer from annotated fields. A mutable field still needs a separate value for each instance. Use field(default_factory=list) to call list each time an instance is created. A factory must create a new value. A factory that returns one existing list still shares that list across instances. Then adding an item to one object changes another object. Dataclasses reject some direct mutable defaults, but a factory can hide the same defect. This task supplies a runnable faulty starter. Repair the shared state while keeping the dataclass model. The result for every box must depend only on actions addressed to that box.

### Worked trace

Create boxes named `left`, `middle`, and `right`. Apply actions `(box 2, "red")`, `(box 0, "blue")`, and `(box 2, "red")`. Required item lists are `["blue"]`, `[]`, and `["red", "red"]`. After each action, only one list may change. A different `Box` object is insufficient if its `items` field refers to the same list as another box.

### Read the existing code

Inspect `Box.items` and the factory used by that field. Follow the list comprehension in `solve` to the append operation. Draw three `Box` objects and arrows to their item lists. Ask when each list is created. Then inspect the output comprehension; it reports the state already stored in each box.

## Your task

### Scoped repair

Repair the initialization of `Box.items`. Keep `Box` as a dataclass. Preserve names order, action order, empty boxes, and repeated items. Do not filter duplicates or rebuild the intended result from the actions at return time. The model itself must have independent state.

### Required behavior

Bug-fix task. `data.names` contains distinct strings in box order. `data.actions` contains objects with valid zero-based `box` index and string `item`. Create one empty box per name, then append each item to its selected box. Return a list of `{"name": string, "items": [strings]}` in names order. Preserve item order and duplicates. The supplied dataclass starter has a factory that returns a shared list. Fix that defect. Empty names implies empty actions. The judge checks isolation behavior, not dataclass syntax.

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

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 04](/problems/cb-04-nested-copy-isolation).

## Examples

### Example 1: one box must not change another

Input to `solve`:
```json
{
  "names": [
    "A",
    "B"
  ],
  "actions": [
    {
      "box": 0,
      "item": "pen"
    }
  ]
}
```
Return:
```json
[
  {
    "name": "A",
    "items": [
      "pen"
    ]
  },
  {
    "name": "B",
    "items": []
  }
]
```

### Example 2: independent item order

Input to `solve`:
```json
{
  "names": [
    "A",
    "B"
  ],
  "actions": [
    {
      "box": 1,
      "item": "book"
    },
    {
      "box": 0,
      "item": "pen"
    },
    {
      "box": 1,
      "item": "paper"
    }
  ]
}
```
Return:
```json
[
  {
    "name": "A",
    "items": [
      "pen"
    ]
  },
  {
    "name": "B",
    "items": [
      "book",
      "paper"
    ]
  }
]
```

### Example 3: no boxes

Input to `solve`:
```json
{
  "names": [],
  "actions": []
}
```
Return:
```json
[]
```

## Constraints

- At most 100 input items. All input values follow the stated contract.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 24 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3.11/library/dataclasses.html#default-factory-functions)
