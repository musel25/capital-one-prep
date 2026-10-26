# 32. Fix a LEFT JOIN that loses customers

[Back to the course list](/?course=capital-one-engineering-50)

**Level 4 · Medium · About 30 minutes**

**Before this problem:** Problem 31; SELECT, WHERE, ordering, and SQL NULL.

## Learn first

A LEFT JOIN keeps each row from its left table even when no right-table row matches. Missing right-side values become NULL. A condition in ON controls which right rows can match. A condition in WHERE runs after the join and can remove those generated NULL rows. This difference often breaks reports that must include customers with no activity. The starter query has that defect. Move the payment qualification to the correct place while preserving the full output contract. A zero amount is a real value, not a missing value. Customers can also share a name, so joins must use their ids rather than display text.

## Your task

Fix the intentionally faulty `report_rows(connection)` query. The scaffold creates `customers(id PRIMARY KEY, name)` and `payments(id PRIMARY KEY, customer_id nullable, amount, status)`. Input supplies the same named fields in customers and payments lists. For every customer, emit one row for each payment with matching customer_id and status paid. If no paid payment matches, emit exactly one row with payment_id and amount null. Ignore orphan payments, null customer_id values, and pending payments. Each output row has `{customer_id, name, payment_id, amount}`. Order by customer_id ascending, then payment_id ascending. Use a LEFT JOIN. The reference executes SQLite. The output judge cannot enforce SQL use or query structure.

## Examples

### Example 1: keep customer with no payments

Input to `solve`:
```json
{
  "customers": [
    {
      "id": 1,
      "name": "1"
    },
    {
      "id": 2,
      "name": "2"
    }
  ],
  "payments": [
    {
      "id": 1,
      "customer_id": 1,
      "amount": 10,
      "status": "paid"
    }
  ]
}
```
Return:
```json
[
  {
    "customer_id": 1,
    "name": "1",
    "payment_id": 1,
    "amount": 10
  },
  {
    "customer_id": 2,
    "name": "2",
    "payment_id": null,
    "amount": null
  }
]
```

### Example 2: pending-only customer remains with nulls

Input to `solve`:
```json
{
  "customers": [
    {
      "id": 1,
      "name": "1"
    }
  ],
  "payments": [
    {
      "id": 1,
      "customer_id": 1,
      "amount": 10,
      "status": "pending"
    }
  ]
}
```
Return:
```json
[
  {
    "customer_id": 1,
    "name": "1",
    "payment_id": null,
    "amount": null
  }
]
```

### Example 3: one output row per paid payment

Input to `solve`:
```json
{
  "customers": [
    {
      "id": 1,
      "name": "1"
    }
  ],
  "payments": [
    {
      "id": 3,
      "customer_id": 1,
      "amount": 30,
      "status": "paid"
    },
    {
      "id": 2,
      "customer_id": 1,
      "amount": 20,
      "status": "paid"
    }
  ]
}
```
Return:
```json
[
  {
    "customer_id": 1,
    "name": "1",
    "payment_id": 2,
    "amount": 20
  },
  {
    "customer_id": 1,
    "name": "1",
    "payment_id": 3,
    "amount": 30
  }
]
```

## Constraints

- 0–200 customers and 0–300 payments. Ids are positive integers at most 1000000 and unique within each table.
- Payment customer_id is null or a positive integer at most 1000000. Foreign keys are intentionally not enforced.
- status is paid or pending. amount is an integer in [-1000000,1000000]. Names have 1–50 printable ASCII characters.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 32 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://www.sqlite.org/lang_select.html#whereclause)
