# 19. Cap partial refunds with exact cents

[Back to the course list](/?course=capital-one-engineering-50)

**Level 2 · Medium · About 25 minutes**

**Before this problem:** Integer cents, dataclasses, and account invariants.

## Learn first

A payment can have several partial refunds. The limit applies to their cumulative total, not to each request in isolation. Store the original charge and the refunded amount, or store a remaining refundable amount. Integer cents keep every subtraction exact. Validate a request before changing state so a failed refund cannot reduce the remaining amount. Keep each payment’s state separate. A request for the exact remaining amount is valid and leaves zero. This exercise also permits zero-cent requests, which succeed without changing the amount. Real refund systems need additional rules for request IDs and external settlement; this task isolates the cumulative amount invariant.

## Your task

`data.payments` maps payment IDs to nonnegative integer charged cents. `data.refunds` contains objects with string `payment` and nonnegative integer `cents`; each payment ID exists. Process requests in order. Accept a refund if its cents are at most that payment’s remaining refundable cents. Subtract only accepted refunds. Zero-cent refunds succeed, including after a full refund. Return `{"accepted": [booleans], "remaining": {payment_id: integer_cents}}`. Preserve all payment IDs, including payments with no refund requests.

## Examples

### Example 1: cumulative cap and failure preservation

Input to `solve`:
```json
{
  "payments": {
    "p": 100
  },
  "refunds": [
    {
      "payment": "p",
      "cents": 30
    },
    {
      "payment": "p",
      "cents": 80
    },
    {
      "payment": "p",
      "cents": 70
    }
  ]
}
```
Return:
```json
{
  "accepted": [
    true,
    false,
    true
  ],
  "remaining": {
    "p": 0
  }
}
```

### Example 2: separate payment state

Input to `solve`:
```json
{
  "payments": {
    "a": 50,
    "b": 20
  },
  "refunds": [
    {
      "payment": "b",
      "cents": 20
    },
    {
      "payment": "a",
      "cents": 10
    }
  ]
}
```
Return:
```json
{
  "accepted": [
    true,
    true
  ],
  "remaining": {
    "a": 40,
    "b": 0
  }
}
```

### Example 3: no payments

Input to `solve`:
```json
{
  "payments": {},
  "refunds": []
}
```
Return:
```json
{
  "accepted": [],
  "remaining": {}
}
```

## Constraints

- At most 30 payments and 100 refund requests. Charged and requested cents are at most 1,000,000,000,000.

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

- [Official documentation 1](https://docs.python.org/3.11/library/dataclasses.html)
- [Official documentation 2](https://docs.python.org/3.11/library/stdtypes.html#numeric-types-int-float-complex)
