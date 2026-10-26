# 11. Fix shared dataclass items

[Back to the course list](/?course=capital-one-engineering-50)

**Level 2 · Easy · About 20 minutes**

**Before this problem:** Classes, lists, and the first ten exercises.

## Learn first

A dataclass can generate an initializer from annotated fields. A mutable field still needs a separate value for each instance. Use field(default_factory=list) to call list each time an instance is created. A factory must create a new value. A factory that returns one existing list still shares that list across instances. Then adding an item to one object changes another object. Dataclasses reject some direct mutable defaults, but a factory can hide the same defect. This task supplies a runnable faulty starter. Repair the shared state while keeping the dataclass model. The result for every box must depend only on actions addressed to that box.

## Your task

Bug-fix task. `data.names` contains distinct strings in box order. `data.actions` contains objects with valid zero-based `box` index and string `item`. Create one empty box per name, then append each item to its selected box. Return a list of `{"name": string, "items": [strings]}` in names order. Preserve item order and duplicates. The supplied dataclass starter has a factory that returns a shared list. Fix that defect. Empty names implies empty actions. The judge checks isolation behavior, not dataclass syntax.

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
