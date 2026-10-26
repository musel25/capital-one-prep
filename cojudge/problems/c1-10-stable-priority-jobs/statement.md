# 10. Schedule jobs with stable priorities

[Back to the course list](/?course=capital-one-engineering-50)

**Level 1 · Medium · About 25 minutes**

**Before this problem:** Lists, dictionaries, and functions.

## Learn first

A heap provides efficient access to the smallest key. heapq uses Python tuple ordering, so a tuple can hold a priority, an insertion sequence, and the job payload. The sequence gives a stable tie rule and prevents the payload from deciding the order. Keep the sequence increasing across all insertions, including after a pop. A heap’s internal list is not globally sorted. If you need a final ordered report, sort a copy or drain a separate heap. Empty pops need an explicit result. This task uses null so the result list still contains one entry for each requested pop.

## Your task

`data.actions` is a list of operations. `{"op":"add","id":string,"priority":integer}` inserts a job. Priority is from -100 through 100; smaller values run first. `{"op":"pop"}` removes the next job and records its ID, or null if the queue is empty. Equal priorities use insertion order. IDs may repeat. Return `{"popped": [IDs_or_null], "pending": [IDs_in_future_pop_order]}`. Add operations do not add an entry to `popped`. Use heapq for practice; the judge checks results.

## Examples

### Example 1: smallest priority first

Input to `solve`:
```json
{
  "actions": [
    {
      "op": "add",
      "id": "slow",
      "priority": 5
    },
    {
      "op": "add",
      "id": "fast",
      "priority": 1
    },
    {
      "op": "pop"
    }
  ]
}
```
Return:
```json
{
  "popped": [
    "fast"
  ],
  "pending": [
    "slow"
  ]
}
```

### Example 2: equal priorities use insertion order

Input to `solve`:
```json
{
  "actions": [
    {
      "op": "add",
      "id": "z",
      "priority": 1
    },
    {
      "op": "add",
      "id": "a",
      "priority": 1
    },
    {
      "op": "pop"
    }
  ]
}
```
Return:
```json
{
  "popped": [
    "z"
  ],
  "pending": [
    "a"
  ]
}
```

### Example 3: empty action list

Input to `solve`:
```json
{
  "actions": []
}
```
Return:
```json
{
  "popped": [],
  "pending": []
}
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

- [Official documentation 1](https://docs.python.org/3.11/library/heapq.html#priority-queue-implementation-notes)
