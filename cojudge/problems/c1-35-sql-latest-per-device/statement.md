# 35. Select the latest row per device

[Back to the course list](/?course=capital-one-engineering-50)

**Level 4 · Hard · About 35 minutes**

**Before this problem:** Problems 31–34; SQL ordering, grouping, and NULL values.

## Learn first

Selecting the latest row in each group needs more than finding the maximum timestamp. Several rows can share that timestamp, and the result must keep values from one chosen row. A window function numbers rows within a partition while keeping their other columns. Partition by device and order each partition from newest to oldest. Add a unique id to resolve timestamp ties. Then select the row numbered one. A cutoff belongs before ranking when the question is the latest eligible row. Filtering only after choosing the overall newest row could remove a device that still has older eligible data.

## Your task

Complete `latest_rows(connection, cutoff)` in the SQLite scaffold. Input rows contain `{id:int, device:string, ts:int, value:int|null}` with globally unique ids. The table is `readings(id PRIMARY KEY, device, ts, value)`. Consider only rows with ts at most cutoff. For each exact device string, select the row with greatest ts, then greatest id on a tie. Retain its value even when null. Devices with no eligible rows are absent. Return `{device,id,ts,value}` rows ordered by device ascending using SQLite's default binary order. Use ROW_NUMBER with PARTITION BY and a deterministic ordering rule. The reference executes a real SQLite window query. The output judge checks behavior; it cannot enforce SQL or window-function use.

## Examples

### Example 1: latest row within each device

Input to `solve`:
```json
{
  "rows": [
    {
      "id": 1,
      "device": "a",
      "ts": 5,
      "value": 10
    },
    {
      "id": 2,
      "device": "a",
      "ts": 9,
      "value": 10
    },
    {
      "id": 3,
      "device": "b",
      "ts": 6,
      "value": 10
    }
  ],
  "cutoff": 100
}
```
Return:
```json
[
  {
    "device": "a",
    "id": 2,
    "ts": 9,
    "value": 10
  },
  {
    "device": "b",
    "id": 3,
    "ts": 6,
    "value": 10
  }
]
```

### Example 2: largest id resolves timestamp tie

Input to `solve`:
```json
{
  "rows": [
    {
      "id": 1,
      "device": "a",
      "ts": 5,
      "value": 10
    },
    {
      "id": 3,
      "device": "a",
      "ts": 5,
      "value": 30
    },
    {
      "id": 2,
      "device": "a",
      "ts": 5,
      "value": 20
    }
  ],
  "cutoff": 100
}
```
Return:
```json
[
  {
    "device": "a",
    "id": 3,
    "ts": 5,
    "value": 30
  }
]
```

### Example 3: cutoff filters before ranking

Input to `solve`:
```json
{
  "rows": [
    {
      "id": 1,
      "device": "a",
      "ts": 5,
      "value": 10
    },
    {
      "id": 2,
      "device": "a",
      "ts": 20,
      "value": 10
    }
  ],
  "cutoff": 10
}
```
Return:
```json
[
  {
    "device": "a",
    "id": 1,
    "ts": 5,
    "value": 10
  }
]
```

## Constraints

- 0–400 rows. Ids are 1–1000000; ts and cutoff are integers from 0 through 1000000.
- Device names have 1–50 printable ASCII characters and are case sensitive.
- value is null or an integer in [-1000000,1000000]. Input row order has no meaning.

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

- [Official documentation 1](https://www.sqlite.org/windowfunctions.html)
- [Official documentation 2](https://docs.python.org/3.11/library/sqlite3.html)
