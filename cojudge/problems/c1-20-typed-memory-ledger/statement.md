# 20. Build a typed in-memory ledger

[Back to the course list](/?course=capital-one-engineering-50)

**Level 2 · Medium · About 35 minutes**

**Before this problem:** Exercises 11–19: object state, invariants, atomic changes, and event IDs.

## Learn first

A small ledger combines several rules that must agree. Account objects hold balances. A ledger object coordinates transfers so one debit and one credit form a complete operation. A TypedDict describes the transfer input, while immutable tuples record event payloads for duplicate checks. The event ID policy must also define failed requests. In this task, the first request reserves its ID even if it has insufficient funds. Retrying it cannot later turn the same ID into a different operation. A new ID is required for a new attempt. Keep duplicate detection before balance changes and check funds before either side of a transfer changes.

## Your task

`data.accounts` maps account IDs to nonnegative integer cents. `data.events` contains `{"id":string,"from":account_id,"to":account_id,"cents":nonnegative_integer}`. Both accounts exist. Process events in order. The first event for an ID stores its payload `(from,to,cents)`. It returns `applied` and transfers cents if the source has enough funds; otherwise it returns `insufficient` and changes no balances. The ID remains stored after either result. A later identical payload returns `duplicate`; a different payload with that ID returns `conflict`. Neither changes balances or the stored payload. A self-transfer checks funds, then leaves balances unchanged. Return `{"status": [strings], "balances": final_account_map}`. Practice typed objects and composition. The judge checks outputs only.

## Examples

### Example 1: transfer, duplicate, and conflict

Input to `solve`:
```json
{
  "accounts": {
    "A": 10,
    "B": 0
  },
  "events": [
    {
      "id": "x",
      "from": "A",
      "to": "B",
      "cents": 4
    },
    {
      "id": "x",
      "from": "A",
      "to": "B",
      "cents": 4
    },
    {
      "id": "x",
      "from": "A",
      "to": "B",
      "cents": 5
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
  "balances": {
    "A": 6,
    "B": 4
  }
}
```

### Example 2: failed ID stays reserved after new funds arrive

Input to `solve`:
```json
{
  "accounts": {
    "A": 0,
    "B": 10
  },
  "events": [
    {
      "id": "x",
      "from": "A",
      "to": "B",
      "cents": 5
    },
    {
      "id": "fund",
      "from": "B",
      "to": "A",
      "cents": 10
    },
    {
      "id": "x",
      "from": "A",
      "to": "B",
      "cents": 5
    },
    {
      "id": "new",
      "from": "A",
      "to": "B",
      "cents": 5
    }
  ]
}
```
Return:
```json
{
  "status": [
    "insufficient",
    "applied",
    "duplicate",
    "applied"
  ],
  "balances": {
    "A": 5,
    "B": 5
  }
}
```

### Example 3: empty ledger

Input to `solve`:
```json
{
  "accounts": {},
  "events": []
}
```
Return:
```json
{
  "status": [],
  "balances": {}
}
```

## Constraints

- At most 30 accounts and 100 events. Initial balances and event cents are at most 1,000,000,000,000. Input objects follow the stated types; runtime boundary validation is outside this task.

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

- [Official documentation 1](https://docs.python.org/3.11/library/typing.html#typing.TypedDict)
- [Official documentation 2](https://docs.python.org/3.11/library/dataclasses.html)
