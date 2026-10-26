# 40. Write an order and its outbox event atomically

[Back to the course list](/?course=capital-one-engineering-50)

**Level 4 · Hard · About 30 minutes**

**Before this problem:** SQL transactions, primary keys, and idempotent requests.

## Learn first

A business write and a message publish cannot normally share a local database transaction. A transactional outbox stores the intended event beside the business record instead. One database transaction inserts both rows. A separate worker can later publish committed outbox rows and retry delivery. This task covers the producer boundary only. A failure after either insert must leave neither row behind. A repeated order ID with the same amount must not create another event. A repeated ID with a different amount is a conflict. Atomic outbox insertion prevents missing event records, but it does not itself guarantee exactly one delivery to consumers.

## Your task

`orders` is an ordered list of `{id, amount, fail}`. `fail` is `none`, `business` (after inserting the order), or `event` (after inserting its outbox row). A committed ID returns `replay` for the same amount or `conflict` for a different amount; do not evaluate the fault for these requests. For a new ID, insert order and outbox rows in one SQLite transaction. Return `failed` and roll back on either injected fault; otherwise return `ok`. Return `{results: [...], orders: [[id, amount], ...], events: [[id, amount], ...]}` with both tables sorted by ASCII ID. Use the supplied schema. There is no publisher or network call. The output judge cannot enforce SQL use.

## Examples

### Example 1: business record and event commit

Input to `solve`:
```json
{
  "orders": [
    {
      "id": "a",
      "amount": 2,
      "fail": "none"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "ok"
  ],
  "orders": [
    [
      "a",
      2
    ]
  ],
  "events": [
    [
      "a",
      2
    ]
  ]
}
```

### Example 2: failure between writes

Input to `solve`:
```json
{
  "orders": [
    {
      "id": "a",
      "amount": 2,
      "fail": "business"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "failed"
  ],
  "orders": [],
  "events": []
}
```

### Example 3: retry creates no duplicate event

Input to `solve`:
```json
{
  "orders": [
    {
      "id": "a",
      "amount": 2,
      "fail": "none"
    },
    {
      "id": "a",
      "amount": 2,
      "fail": "none"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "ok",
    "replay"
  ],
  "orders": [
    [
      "a",
      2
    ]
  ],
  "events": [
    [
      "a",
      2
    ]
  ]
}
```

## Constraints

- 0–200 orders. IDs are nonempty ASCII strings of length at most 30.
- Amounts are integer minor units from 1 to 1000000.
- The trace is sequential; it does not test real concurrent transactions.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 36 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://www.sqlite.org/lang_transaction.html)
- [Official documentation 2](https://docs.python.org/3.11/library/sqlite3.html)
