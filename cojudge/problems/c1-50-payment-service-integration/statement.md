# 50. Compose a bounded reliable payment service

[Back to the course list](/?course=capital-one-engineering-50)

**Level 5 · Hard · About 45 minutes**

**Before this problem:** Atomic transfers, idempotency payloads, and transactional outbox records.

## Learn first

A reliable payment boundary combines rules that are easy to implement incorrectly in isolation. The idempotency key identifies the complete request payload, including both accounts and the amount. A successful payment changes two balances, records that key, and creates an event as one logical commit. Replays return before checking the current balance because the original payment already happened. Failed attempts retain no key, so they can retry after recovery. This bounded exercise stages changes in memory and publishes them only after all fault points pass. It is a deterministic event trace, not an actual parallel, thread, or network test. Production storage would need a real durable transaction.

## Your task

`balances` maps existing account IDs to nonnegative integer balances. `payments` contains `{key, from, to, amount, fail}`. The two account IDs exist and differ; amount is positive. First check committed keys: the same (from, to, amount) returns `replay`, while any difference returns `conflict`. These checks ignore fail and current funds. For a new key, insufficient source funds returns `insufficient` without storing the key. Otherwise stage the debit, credit, key, and outbox event as one atomic operation. `fail` is `none`, `debit` (after staging debit), or `outbox` (after preparing the event). Either fault returns `failed` and leaves all committed state unchanged. A successful commit returns `ok`. Return `{results: [...], balances: {...}, events: [[key, from, to, amount], ...]}`. Events follow successful commit order. Failed requests reserve no keys, and no network delivery is required.

## Examples

### Example 1: payment commits balance changes and event

Input to `solve`:
```json
{
  "balances": {
    "a": 5,
    "b": 0
  },
  "payments": [
    {
      "key": "k",
      "from": "a",
      "to": "b",
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
  "balances": {
    "a": 3,
    "b": 2
  },
  "events": [
    [
      "k",
      "a",
      "b",
      2
    ]
  ]
}
```

### Example 2: retry has no duplicate effect or event

Input to `solve`:
```json
{
  "balances": {
    "a": 5,
    "b": 0
  },
  "payments": [
    {
      "key": "k",
      "from": "a",
      "to": "b",
      "amount": 2,
      "fail": "none"
    },
    {
      "key": "k",
      "from": "a",
      "to": "b",
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
  "balances": {
    "a": 3,
    "b": 2
  },
  "events": [
    [
      "k",
      "a",
      "b",
      2
    ]
  ]
}
```

### Example 3: retry after partial staged debit

Input to `solve`:
```json
{
  "balances": {
    "a": 5,
    "b": 0
  },
  "payments": [
    {
      "key": "k",
      "from": "a",
      "to": "b",
      "amount": 2,
      "fail": "debit"
    },
    {
      "key": "k",
      "from": "a",
      "to": "b",
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
    "failed",
    "ok"
  ],
  "balances": {
    "a": 3,
    "b": 2
  },
  "events": [
    [
      "k",
      "a",
      "b",
      2
    ]
  ]
}
```

## Constraints

- 0–100 accounts and 0–300 payments. IDs and keys are nonempty ASCII strings.
- Initial balances are 0–1000000 and amounts are 1–1000000.
- Implement only this bounded state model; no HTTP server, database setup, or background worker is required.

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

- [Official documentation 1](https://www.sqlite.org/lang_transaction.html)
- [Official documentation 2](https://docs.python.org/3.11/library/copy.html)
