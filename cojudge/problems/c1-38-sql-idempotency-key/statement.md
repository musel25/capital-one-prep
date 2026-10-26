# 38. Commit a credit and its idempotency key

[Back to the course list](/?course=capital-one-engineering-50)

**Level 4 · Medium · About 30 minutes**

**Before this problem:** Transactions, UNIQUE constraints, and request retries.

## Learn first

A retry can arrive after the first request has already committed. An idempotency key identifies that logical request. Store the key and its payload in a table with a uniqueness constraint. A repeat with the same payload returns a replay result. A repeat with a different payload is a conflict. The key and the business write must share one transaction. Otherwise a crash can record the key without applying the credit, or apply the credit without recording the key. A failed transaction leaves the key available for a later attempt. This task models ordered requests and an injected failure immediately before commit.

## Your task

`balance` is the initial account balance. `credits` contains `{key, amount, fail}` objects. For a committed key, return `replay` for the same amount or `conflict` for a different amount, with no change. For a new key, atomically insert the key and add its amount. If `fail` is true, roll back both writes and return `failed`; otherwise commit and return `ok`. Return `{results: [...], balance: integer, keys: [...]}`. Sort committed keys in ASCII order. Key checks take precedence over injected failures. Use the supplied SQLite tables. SQL use cannot be certified by the output judge.

## Examples

### Example 1: new credit

Input to `solve`:
```json
{
  "balance": 0,
  "credits": [
    {
      "key": "k",
      "amount": 2,
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
  "balance": 2,
  "keys": [
    "k"
  ]
}
```

### Example 2: retry does not add money

Input to `solve`:
```json
{
  "balance": 0,
  "credits": [
    {
      "key": "k",
      "amount": 2,
      "fail": false
    },
    {
      "key": "k",
      "amount": 2,
      "fail": false
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
  "balance": 2,
  "keys": [
    "k"
  ]
}
```

### Example 3: key cannot change amount

Input to `solve`:
```json
{
  "balance": 0,
  "credits": [
    {
      "key": "k",
      "amount": 2,
      "fail": false
    },
    {
      "key": "k",
      "amount": 3,
      "fail": false
    }
  ]
}
```
Return:
```json
{
  "results": [
    "ok",
    "conflict"
  ],
  "balance": 2,
  "keys": [
    "k"
  ]
}
```

## Constraints

- 0–200 credits. Balance is 0–1000000; amounts are 1–1000000.
- Keys are nonempty ASCII strings of length at most 30. fail is Boolean.
- This ordered trace does not test actual parallel transactions.

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

- [Official documentation 1](https://www.sqlite.org/lang_createtable.html)
- [Official documentation 2](https://docs.python.org/3.11/library/sqlite3.html)
