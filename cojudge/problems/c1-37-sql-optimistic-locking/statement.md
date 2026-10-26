# 37. Reject stale SQL updates

[Back to the course list](/?course=capital-one-engineering-50)

**Level 4 · Medium · About 25 minutes**

**Before this problem:** SQL UPDATE and transaction basics.

## Learn first

A client can read a document and then write after another client has changed it. A version number lets the database detect that stale write. The client sends the version it read. One UPDATE statement checks that version, changes the value, and increments the version. If the statement changes no rows, the client must refresh its data before it retries. Checking the version in a separate read is not the same guarantee: another writer could run between the read and write. This exercise supplies an ordered trace of client proposals. Even a write of the same value counts as an accepted update and advances the version.

## Your task

`value` is the initial document string and `version` is its initial integer version. Each item in `updates` has a string `value` and integer `expected`. Accept it only when `expected` equals the current version. On acceptance replace the value and increment the version by one. Rejections change nothing. Return `{accepted: [Boolean, ...], value: string, version: integer}`. Complete the SQL update loop in the scaffold. This is a deterministic proposal trace, not an actual parallel execution test. The output judge cannot enforce SQL syntax or architecture.

## Examples

### Example 1: matching version updates

Input to `solve`:
```json
{
  "version": 0,
  "value": "old",
  "updates": [
    {
      "expected": 0,
      "value": "new"
    }
  ]
}
```
Return:
```json
{
  "accepted": [
    true
  ],
  "value": "new",
  "version": 1
}
```

### Example 2: stale writer is rejected

Input to `solve`:
```json
{
  "version": 2,
  "value": "old",
  "updates": [
    {
      "expected": 1,
      "value": "new"
    }
  ]
}
```
Return:
```json
{
  "accepted": [
    false
  ],
  "value": "old",
  "version": 2
}
```

### Example 3: two readers share a version

Input to `solve`:
```json
{
  "version": 0,
  "value": "old",
  "updates": [
    {
      "expected": 0,
      "value": "one"
    },
    {
      "expected": 0,
      "value": "two"
    }
  ]
}
```
Return:
```json
{
  "accepted": [
    true,
    false
  ],
  "value": "one",
  "version": 1
}
```

## Constraints

- 0–200 updates. Versions and expected versions are 0–1000000.
- Values are ASCII strings of length 0–100.

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

- [Official documentation 1](https://www.sqlite.org/lang_update.html)
- [Official documentation 2](https://docs.python.org/3.11/library/sqlite3.html)
