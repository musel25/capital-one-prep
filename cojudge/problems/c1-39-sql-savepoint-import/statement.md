# 39. Isolate failed import rows with savepoints

[Back to the course list](/?course=capital-one-engineering-50)

**Level 4 · Hard · About 35 minutes**

**Before this problem:** Transactions, constraint failures, and exception handling.

## Learn first

A savepoint marks a position inside a transaction. ROLLBACK TO restores that position without discarding earlier work in the transaction. RELEASE removes the savepoint. It does not make inner changes durable when an outer transaction is still open. This is useful for batch imports: one bad row can fail while other rows remain eligible to commit. The final batch decision still controls all accepted rows. A row can also fail after its insert succeeds. In that case the savepoint must remove that inserted row before the next item runs. Keep row outcomes separate from the final batch commit decision.

## Your task

`batches` is an ordered list of `{rows, abort}`. Each row is `{id, qty, fail}`. Use the supplied SQLite table. Each batch starts an outer transaction. Attempt each row under its own savepoint. A duplicate ID or negative quantity gives `invalid`. Otherwise insert it; if `fail` is true, undo that insert and give `failed`. Successful row attempts give `ok`. Continue after every row failure. If `abort` is true, roll back the whole batch; otherwise commit it. Return `{batches: [{rows: [status, ...], committed: Boolean}, ...], rows: [[id, qty], ...]}`. Row statuses describe attempts even when the batch later aborts. Sort final rows by ASCII ID. Constraint errors take precedence over injected failures. The judge cannot verify SQL use.

## Examples

### Example 1: valid item commits

Input to `solve`:
```json
{
  "batches": [
    {
      "rows": [
        {
          "id": "a",
          "qty": 1,
          "fail": false
        }
      ],
      "abort": false
    }
  ]
}
```
Return:
```json
{
  "batches": [
    {
      "rows": [
        "ok"
      ],
      "committed": true
    }
  ],
  "rows": [
    [
      "a",
      1
    ]
  ]
}
```

### Example 2: one invalid item does not cancel batch

Input to `solve`:
```json
{
  "batches": [
    {
      "rows": [
        {
          "id": "a",
          "qty": 1,
          "fail": false
        },
        {
          "id": "b",
          "qty": -1,
          "fail": false
        },
        {
          "id": "c",
          "qty": 3,
          "fail": false
        }
      ],
      "abort": false
    }
  ]
}
```
Return:
```json
{
  "batches": [
    {
      "rows": [
        "ok",
        "invalid",
        "ok"
      ],
      "committed": true
    }
  ],
  "rows": [
    [
      "a",
      1
    ],
    [
      "c",
      3
    ]
  ]
}
```

### Example 3: outer abort cancels released savepoint

Input to `solve`:
```json
{
  "batches": [
    {
      "rows": [
        {
          "id": "a",
          "qty": 1,
          "fail": false
        }
      ],
      "abort": true
    }
  ]
}
```
Return:
```json
{
  "batches": [
    {
      "rows": [
        "ok"
      ],
      "committed": false
    }
  ],
  "rows": []
}
```

## Constraints

- 0–30 batches, each with 0–30 rows.
- IDs are nonempty ASCII strings. Quantities are -100–1000000. fail and abort are Boolean.
- No actual concurrent transactions occur.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 37 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://www.sqlite.org/lang_savepoint.html)
- [Official documentation 2](https://docs.python.org/3.11/library/sqlite3.html)
