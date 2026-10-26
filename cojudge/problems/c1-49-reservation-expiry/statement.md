# 49. Expire reservations and make transitions idempotent

[Back to the course list](/?course=capital-one-engineering-50)

**Level 5 · Hard · About 40 minutes**

**Before this problem:** State machines, inventory invariants, and idempotency.

## Learn first

A reservation temporarily removes stock from the available pool. Confirmation makes that allocation permanent. Release or expiry returns the held stock, but must do so only once. Terminal states prevent repeated commands from creating extra stock. An idempotent reserve retry also must not extend the original deadline. Here each accepted reservation retains its ID, payload, and final state. Insufficient attempts create no record and may retry later. Expire held records before processing every command, including commands for another ID. This makes the exact expiry boundary explicit. The task is a deterministic event trace, not an actual parallel, thread, or network test.

## Your task

Start with integer `stock`. `ops` have nondecreasing `at`, `id`, and `op`. Before each operation, change every held reservation with `expires <= at` to `expired` and restore its quantity. `reserve` also has positive `qty` and `ttl`. For an existing ID, return its current state if qty and ttl match, otherwise `conflict`; do not extend expiry. For a new ID, return `insufficient` without a record if stock is too low. Otherwise subtract qty, set expiry to at + ttl, store state `held`, and return `held`. `confirm` changes held to `confirmed` without restoring stock. `release` changes held to `released` and restores stock once. Both return the resulting current state, or `missing` for an unknown ID. Confirmed, released, and expired states are permanent. Return `{results: [...], available: integer, reservations: [[id, state], ...]}` sorted by ASCII ID.

## Examples

### Example 1: confirm before expiry consumes stock

Input to `solve`:
```json
{
  "stock": 5,
  "ops": [
    {
      "op": "reserve",
      "at": 0,
      "id": "a",
      "qty": 2,
      "ttl": 5
    },
    {
      "op": "confirm",
      "at": 4,
      "id": "a"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "held",
    "confirmed"
  ],
  "available": 3,
  "reservations": [
    [
      "a",
      "confirmed"
    ]
  ]
}
```

### Example 2: confirmation at expiry is too late

Input to `solve`:
```json
{
  "stock": 5,
  "ops": [
    {
      "op": "reserve",
      "at": 0,
      "id": "a",
      "qty": 2,
      "ttl": 5
    },
    {
      "op": "confirm",
      "at": 5,
      "id": "a"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "held",
    "expired"
  ],
  "available": 5,
  "reservations": [
    [
      "a",
      "expired"
    ]
  ]
}
```

### Example 3: release restores stock only once

Input to `solve`:
```json
{
  "stock": 5,
  "ops": [
    {
      "op": "reserve",
      "at": 0,
      "id": "a",
      "qty": 2,
      "ttl": 5
    },
    {
      "op": "release",
      "at": 1,
      "id": "a"
    },
    {
      "op": "release",
      "at": 2,
      "id": "a"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "held",
    "released",
    "released"
  ],
  "available": 5,
  "reservations": [
    [
      "a",
      "released"
    ]
  ]
}
```

## Constraints

- Stock is 0–1000000. There are 0–300 operations.
- Times are 0–1000000; qty and ttl are 1–1000000. IDs are nonempty ASCII strings.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 39 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3.11/library/enum.html)
- [Official documentation 2](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)
