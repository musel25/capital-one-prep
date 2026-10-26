# 36. Repair an atomic SQL transfer

[Back to the course list](/?course=capital-one-engineering-50)

**Level 4 · Medium · About 30 minutes**

**Before this problem:** SQL UPDATE, parameterized statements, and Python exceptions.

## Learn first

A transfer changes two balances. Both changes must commit, or neither change must remain. A transaction groups these writes into one unit. Commit only after the debit and credit succeed. Roll back if an exception occurs between them. A conditional debit can check the available balance and subtract the amount in one statement. Its affected-row count tells you whether the debit occurred. Setup writes also need a commit before you start an explicit transaction. This exercise injects a failure after the debit. The starter catches that failure but commits the partial transfer. Repair that transaction boundary and preserve earlier successful transfers.

## Your task

Repair the faulty `solve(data)` implementation. `balances` maps account IDs to initial integer balances. `transfers` is an ordered list of objects with `from`, `to`, positive `amount`, and Boolean `fail`. Both IDs exist and differ. First reject a transfer that lacks funds with `insufficient`. Otherwise debit the source. If `fail` is true, roll back and return `failed`. Otherwise credit the destination, commit, and return `ok`. Each transfer has its own transaction. Return `{results: [...], balances: {...}}` with one status per transfer and final balances. Use the supplied in-memory SQLite setup. The output judge cannot verify SQL use.

## Examples

### Example 1: transfer commits both entries

Input to `solve`:
```json
{
  "balances": {
    "a": 10,
    "b": 0
  },
  "transfers": [
    {
      "from": "a",
      "to": "b",
      "amount": 4,
      "fail": false
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
  "balances": {
    "a": 6,
    "b": 4
  }
}
```

### Example 2: failure restores debit

Input to `solve`:
```json
{
  "balances": {
    "a": 10,
    "b": 0
  },
  "transfers": [
    {
      "from": "a",
      "to": "b",
      "amount": 4,
      "fail": true
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
  "balances": {
    "a": 10,
    "b": 0
  }
}
```

### Example 3: insufficient funds change neither balance

Input to `solve`:
```json
{
  "balances": {
    "a": 3,
    "b": 2
  },
  "transfers": [
    {
      "from": "a",
      "to": "b",
      "amount": 4,
      "fail": false
    }
  ]
}
```
Return:
```json
{
  "results": [
    "insufficient"
  ],
  "balances": {
    "a": 3,
    "b": 2
  }
}
```

## Constraints

- 0–100 accounts and 0–200 transfers.
- IDs are nonempty ASCII strings. Initial balances are 0–1000000; amounts are 1–1000000.
- Failures are injected exceptions, not actual concurrent operations.

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

- [Official documentation 1](https://docs.python.org/3.11/library/sqlite3.html)
- [Official documentation 2](https://www.sqlite.org/lang_transaction.html)
