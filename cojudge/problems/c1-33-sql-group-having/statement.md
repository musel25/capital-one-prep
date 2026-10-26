# 33. Summarize groups without losing NULL meaning

[Back to the course list](/?course=capital-one-engineering-50)

**Level 4 · Medium · About 35 minutes**

**Before this problem:** Problems 31–32; filtering, NULL, and deterministic output order.

## Learn first

Aggregation combines several rows into one summary. WHERE selects source rows before grouping. HAVING selects completed groups using aggregate values. COUNT(*) counts rows, while COUNT(amount) counts only rows whose amount is not NULL. SUM ignores NULL amounts and returns NULL when every amount in a group is NULL. A report can explicitly replace that result with zero through COALESCE. Equal amounts in different entries are still separate business events. Adding DISTINCT would change their meaning. This exercise asks for both row count and known-value count so that missing amounts remain visible even when the displayed total defaults to zero.

## Your task

Complete `summary_rows(connection, minimum_total, minimum_events)`. The scaffold loads `entries(id PRIMARY KEY, account, amount nullable, kind)` from `rows`. First keep only kind paid. Group by exact account string. For each group calculate events as all paid rows, valued as paid rows with non-null amount, and total as the sum of non-null amounts, or zero if all are null. Keep groups with total at least minimum_total and events at least minimum_events. Accounts with no paid rows do not form groups. Return `{account, events, valued, total}` rows ordered by total descending, then account ascending with SQLite's default binary ordering. Use SQL aggregation and HAVING with bound thresholds. The reference executes SQLite. The output judge cannot enforce SQL use or the chosen clauses.

## Examples

### Example 1: repeated amounts count and null affects only valued count

Input to `solve`:
```json
{
  "rows": [
    {
      "id": 1,
      "account": "a",
      "amount": 10,
      "kind": "paid"
    },
    {
      "id": 2,
      "account": "a",
      "amount": 10,
      "kind": "paid"
    },
    {
      "id": 3,
      "account": "a",
      "amount": null,
      "kind": "paid"
    }
  ],
  "minimum_total": 0,
  "minimum_events": 1
}
```
Return:
```json
[
  {
    "account": "a",
    "events": 3,
    "valued": 2,
    "total": 20
  }
]
```

### Example 2: HAVING applies both group thresholds

Input to `solve`:
```json
{
  "rows": [
    {
      "id": 1,
      "account": "a",
      "amount": 4,
      "kind": "paid"
    },
    {
      "id": 2,
      "account": "a",
      "amount": 6,
      "kind": "paid"
    },
    {
      "id": 3,
      "account": "b",
      "amount": 20,
      "kind": "paid"
    }
  ],
  "minimum_total": 10,
  "minimum_events": 2
}
```
Return:
```json
[
  {
    "account": "a",
    "events": 2,
    "valued": 2,
    "total": 10
  }
]
```

### Example 3: all-null sum becomes zero

Input to `solve`:
```json
{
  "rows": [
    {
      "id": 1,
      "account": "a",
      "amount": null,
      "kind": "paid"
    },
    {
      "id": 2,
      "account": "a",
      "amount": null,
      "kind": "paid"
    }
  ],
  "minimum_total": 0,
  "minimum_events": 1
}
```
Return:
```json
[
  {
    "account": "a",
    "events": 2,
    "valued": 0,
    "total": 0
  }
]
```

## Constraints

- 0–300 rows with unique ids from 1 through 1000000.
- account is a nonempty printable ASCII string of at most 40 characters. kind is paid or void.
- amount is null or an integer in [-1000000,1000000]. minimum_total is in [-300000000,300000000]; minimum_events is 1–300.

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

- [Official documentation 1](https://www.sqlite.org/lang_aggfunc.html)
- [Official documentation 2](https://www.sqlite.org/lang_select.html#resultset)
