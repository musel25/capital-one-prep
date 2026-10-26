# 17. Fix an in-memory transfer batch

[Back to the course list](/?course=capital-one-engineering-50)

**Level 2 · Medium · About 25 minutes**

**Before this problem:** Dictionary copies, account invariants, and ordered operations.

## Learn first

Atomic means that an operation has one complete result: all intended changes happen, or none happen. A loop that updates live balances can leave a partial result when a later transfer fails. For a small in-memory model, start with a working copy. Apply each transfer to that copy in order. Earlier transfers in the same batch can fund later transfers. Publish the working copy only after every transfer succeeds. On failure, discard it. This method is a simulation of atomic behavior within one call. It does not create a database transaction or protect the state from concurrent callers.

## Your task

Bug-fix task. `data.accounts` maps account IDs to nonnegative integer cents. `data.batches` is a list of transfer lists. Each transfer has string `from`, string `to`, and nonnegative integer `cents`. Both accounts always exist. Process batches in order. Within a batch, process transfers in order using the tentative updated balances. If any source has less than cents, reject the entire batch and restore its starting balances. Otherwise accept all transfers. A self-transfer needs enough funds but leaves its balance unchanged. An empty batch succeeds. Return `{"accepted": [booleans_per_batch], "balances": final_account_map}`. Repair the starter’s partial-write defect.

## Examples

### Example 1: late failure rolls back earlier transfer

Input to `solve`:
```json
{
  "accounts": {
    "A": 10,
    "B": 0
  },
  "batches": [
    [
      {
        "from": "A",
        "to": "B",
        "cents": 6
      },
      {
        "from": "A",
        "to": "B",
        "cents": 5
      }
    ]
  ]
}
```
Return:
```json
{
  "accepted": [
    false
  ],
  "balances": {
    "A": 10,
    "B": 0
  }
}
```

### Example 2: earlier transfer funds later transfer

Input to `solve`:
```json
{
  "accounts": {
    "A": 10,
    "B": 0,
    "C": 0
  },
  "batches": [
    [
      {
        "from": "A",
        "to": "B",
        "cents": 7
      },
      {
        "from": "B",
        "to": "C",
        "cents": 7
      }
    ]
  ]
}
```
Return:
```json
{
  "accepted": [
    true
  ],
  "balances": {
    "A": 3,
    "B": 0,
    "C": 7
  }
}
```

### Example 3: no accounts or batches

Input to `solve`:
```json
{
  "accounts": {},
  "batches": []
}
```
Return:
```json
{
  "accepted": [],
  "balances": {}
}
```

## Constraints

- At most 30 accounts, 30 batches, and 100 transfers per batch. Input cents and initial balances are at most 1,000,000,000,000.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 25 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3.11/library/stdtypes.html#dict.copy)
