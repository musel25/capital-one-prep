# 18. Separate duplicate events from conflicts

[Back to the course list](/?course=capital-one-engineering-50)

**Level 2 · Medium · About 25 minutes**

**Before this problem:** Dictionaries, event processing, and signed integer arithmetic.

## Learn first

An event ID can make a retried operation safe to handle more than once. Store the payload associated with the first use of that ID. If a later event has the same ID and the same payload, it is a duplicate and must not apply again. If it has a different payload, it is a conflict. Ignoring that distinction can hide a caller bug or apply an unintended change. Do not replace the stored payload when a conflict arrives. The first event remains the reference for later comparisons. This task uses a single signed delta as the payload, so equality has one clear meaning.

## Your task

`data.balance` is an integer starting total. `data.events` contains objects with string `id` and integer `delta`. Signed totals and deltas are permitted. On the first occurrence of an ID, add its delta and record status `applied`. For an existing ID, record `duplicate` if delta equals its first delta; otherwise record `conflict`. Neither duplicate nor conflict changes the total or stored first delta. Return `{"status": [status_strings], "balance": final_integer}` in event order.

## Examples

### Example 1: new, duplicate, and conflicting payload

Input to `solve`:
```json
{
  "balance": 10,
  "events": [
    {
      "id": "e1",
      "delta": 5
    },
    {
      "id": "e1",
      "delta": 5
    },
    {
      "id": "e1",
      "delta": 7
    }
  ]
}
```
Return:
```json
{
  "status": [
    "applied",
    "duplicate",
    "conflict"
  ],
  "balance": 15
}
```

### Example 2: conflict does not replace the first payload

Input to `solve`:
```json
{
  "balance": 0,
  "events": [
    {
      "id": "x",
      "delta": 2
    },
    {
      "id": "x",
      "delta": 3
    },
    {
      "id": "x",
      "delta": 2
    }
  ]
}
```
Return:
```json
{
  "status": [
    "applied",
    "conflict",
    "duplicate"
  ],
  "balance": 2
}
```

### Example 3: no events

Input to `solve`:
```json
{
  "balance": 8,
  "events": []
}
```
Return:
```json
{
  "status": [],
  "balance": 8
}
```

## Constraints

- At most 100 events. Initial total and deltas have absolute value at most 1,000,000,000,000.

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

- [Official documentation 1](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)
