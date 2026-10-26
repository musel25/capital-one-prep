# 34. Create accounts with stable conflict rules

[Back to the course list](/?course=capital-one-engineering-50)

**Level 4 · Medium · About 35 minutes**

**Before this problem:** Problems 24 and 31–33; replay semantics, SQLite placeholders, and queries.

## Learn first

A unique database constraint is the final guard against duplicate keys. Checking for a row in application code before inserting it is not enough when concurrent writers exist. An insert can instead use a conflict policy tied to the unique key. This exercise keeps the first stored value. The application then distinguishes a matching repeated request from a request that tries to change that value. Use bound parameters even when the schema is small. Quotes and SQL punctuation can appear in a valid username. The simulation is sequential, so it demonstrates the constraint and result policy without claiming to test concurrent transactions or durable storage.

## Your task

Complete `create_account(connection, username, quota)` in the SQLite scaffold. Input initial is a list of unique `{username:string, quota:int}` records. requests contains records of the same shape and may repeat names. The table has `username TEXT PRIMARY KEY NOT NULL` and quota INTEGER NOT NULL, with default case-sensitive text comparison. A new username inserts the row and returns `{status:201, record:stored_row}`. An existing username with the same quota returns status 200. A different quota returns status 409. Both existing-name cases leave the row unchanged and return its original record. Use a parameterized insert with a uniqueness conflict policy and a parameterized lookup. The scaffold returns responses in input order and final accounts in username order. The reference executes SQLite. The output judge cannot enforce SQL use or parameter binding.

## Examples

### Example 1: duplicate identical create is a replay

Input to `solve`:
```json
{
  "initial": [],
  "requests": [
    {
      "username": "ada",
      "quota": 10
    },
    {
      "username": "ada",
      "quota": 10
    }
  ]
}
```
Return:
```json
{
  "responses": [
    {
      "status": 201,
      "record": {
        "username": "ada",
        "quota": 10
      }
    },
    {
      "status": 200,
      "record": {
        "username": "ada",
        "quota": 10
      }
    }
  ],
  "accounts": [
    {
      "username": "ada",
      "quota": 10
    }
  ]
}
```

### Example 2: conflicting quota preserves original

Input to `solve`:
```json
{
  "initial": [
    {
      "username": "ada",
      "quota": 10
    }
  ],
  "requests": [
    {
      "username": "ada",
      "quota": 20
    }
  ]
}
```
Return:
```json
{
  "responses": [
    {
      "status": 409,
      "record": {
        "username": "ada",
        "quota": 10
      }
    }
  ],
  "accounts": [
    {
      "username": "ada",
      "quota": 10
    }
  ]
}
```

### Example 3: quote in bound username

Input to `solve`:
```json
{
  "initial": [],
  "requests": [
    {
      "username": "O'Reilly",
      "quota": 10
    }
  ]
}
```
Return:
```json
{
  "responses": [
    {
      "status": 201,
      "record": {
        "username": "O'Reilly",
        "quota": 10
      }
    }
  ],
  "accounts": [
    {
      "username": "O'Reilly",
      "quota": 10
    }
  ]
}
```

## Constraints

- 0–200 initial accounts and 0–300 requests. Initial usernames are unique with exact case.
- Usernames have 1–80 printable ASCII characters; quotes, spaces, and SQL punctuation are valid.
- Quota is an integer from 0 through 1000000. All records contain exactly username and quota.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 31 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://www.sqlite.org/lang_upsert.html)
- [Official documentation 2](https://docs.python.org/3.11/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries)
