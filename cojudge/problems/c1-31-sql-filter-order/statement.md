# 31. Query posted transfers safely

[Back to the course list](/?course=capital-one-engineering-50)

**Level 4 · Medium · About 30 minutes**

**Before this problem:** Problems 1–30; Python functions and API input boundaries. No prior SQL is required.

## Learn first

SQL describes the rows you want from a table. SELECT chooses output columns. WHERE keeps rows that meet a condition. ORDER BY defines their result order, and LIMIT bounds the number returned. Without a complete ordering rule, equal values can appear in an unstable order. Add a unique id as a tie breaker. Python's sqlite3 module passes query values separately through placeholders. A name containing a quote must remain a value rather than become part of SQL text. The supplied code creates an in-memory database and loads the input. Your task is to write the selection query, not database setup code.

## Your task

Complete `select_rows(connection, owner, minimum, limit)` in the supplied SQLite scaffold. `rows` contains `{id:int, owner:string, amount:int, posted:bool}`; ids are unique. The table is `transfers(id, owner, amount, posted)` with posted stored as 0 or 1. Select rows whose owner equals the supplied owner exactly, posted is 1, and amount is at least minimum. Order by amount descending, then id ascending. Return at most limit rows with only id and amount. The scaffold turns query rows into the output list. Use bound parameters for owner, minimum, and limit. The reference executes real SQLite queries. The output judge checks results; it cannot enforce SQL use or parameter binding.

## Examples

### Example 1: sort before taking limit

Input to `solve`:
```json
{
  "rows": [
    {
      "id": 3,
      "amount": 20,
      "owner": "a",
      "posted": true
    },
    {
      "id": 1,
      "amount": 20,
      "owner": "a",
      "posted": true
    },
    {
      "id": 2,
      "amount": 10,
      "owner": "a",
      "posted": true
    }
  ],
  "owner": "a",
  "minimum": 0,
  "limit": 2
}
```
Return:
```json
[
  {
    "id": 1,
    "amount": 20
  },
  {
    "id": 3,
    "amount": 20
  }
]
```

### Example 2: quoted owner is a bound value

Input to `solve`:
```json
{
  "rows": [
    {
      "id": 1,
      "amount": 5,
      "owner": "O'Reilly",
      "posted": true
    },
    {
      "id": 2,
      "amount": 9,
      "owner": "a",
      "posted": true
    }
  ],
  "owner": "O'Reilly",
  "minimum": 0,
  "limit": 10
}
```
Return:
```json
[
  {
    "id": 1,
    "amount": 5
  }
]
```

### Example 3: inclusive minimum and posted filter

Input to `solve`:
```json
{
  "rows": [
    {
      "id": 1,
      "amount": 10,
      "owner": "a",
      "posted": true
    },
    {
      "id": 2,
      "amount": 9,
      "owner": "a",
      "posted": true
    },
    {
      "id": 3,
      "amount": 20,
      "owner": "a",
      "posted": false
    }
  ],
  "owner": "a",
  "minimum": 10,
  "limit": 10
}
```
Return:
```json
[
  {
    "id": 1,
    "amount": 10
  }
]
```

## Constraints

- 0–300 rows; ids are 1–1000000. amount and minimum are integers in [-1000000,1000000].
- limit is 0–100. Owner strings have 1–80 printable ASCII characters, including possible quotes and SQL punctuation.
- All input rows meet the schema; there are no duplicate ids or null fields.

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

- [Official documentation 1](https://docs.python.org/3.11/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries)
- [Official documentation 2](https://www.sqlite.org/lang_select.html)
