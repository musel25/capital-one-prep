# 25. Page by timestamp and id

[Back to the course list](/?course=capital-one-engineering-50)

**Level 3 · Medium · About 35 minutes**

**Before this problem:** Problems 21–24; tuple ordering and state changes.

## Learn first

Offset pagination counts how many rows to skip. An insertion before that position can shift later pages. A cursor can instead store the final ordering key from the previous page. The next query asks for keys strictly after that key. A timestamp alone is not sufficient when records share a timestamp. Add a unique id to create a total order. This exercise makes the cursor visible as a pair so the ordering rule is easy to inspect. New records after the cursor can appear in later results. Records inserted before it will not appear there. Cursor pagination alone does not create a database snapshot.

## Your task

`records` is a list of `{id:int, ts:int}`. `actions` contains inserts `{op:"insert", record:{id,ts}}` and page requests `{op:"page", after:null|[ts,id], limit:int}`. Inserted ids are globally unique. For each page, use current records ordered by ascending `(ts,id)`. If after is non-null, keep only keys strictly greater than it. Take at most limit records. Return `{ids:[...], next:cursor}` for that page. Set next to the final selected `[ts,id]` only if more eligible records remain. Otherwise next is null, including an empty page. A cursor need not name an existing record. Return only page responses; inserts produce none. Each page uses its supplied cursor independently.

## Examples

### Example 1: timestamp ties use id

Input to `solve`:
```json
{
  "records": [
    {
      "id": 3,
      "ts": 2
    },
    {
      "id": 2,
      "ts": 1
    },
    {
      "id": 1,
      "ts": 1
    }
  ],
  "actions": [
    {
      "op": "page",
      "after": null,
      "limit": 2
    }
  ]
}
```
Return:
```json
[
  {
    "ids": [
      1,
      2
    ],
    "next": [
      1,
      2
    ]
  }
]
```

### Example 2: insertion before cursor does not shift page

Input to `solve`:
```json
{
  "records": [
    {
      "id": 1,
      "ts": 10
    },
    {
      "id": 2,
      "ts": 20
    }
  ],
  "actions": [
    {
      "op": "page",
      "after": null,
      "limit": 1
    },
    {
      "op": "insert",
      "record": {
        "id": 3,
        "ts": 5
      }
    },
    {
      "op": "page",
      "after": [
        10,
        1
      ],
      "limit": 1
    }
  ]
}
```
Return:
```json
[
  {
    "ids": [
      1
    ],
    "next": [
      10,
      1
    ]
  },
  {
    "ids": [
      2
    ],
    "next": null
  }
]
```

### Example 3: new row after cursor can appear

Input to `solve`:
```json
{
  "records": [
    {
      "id": 1,
      "ts": 10
    },
    {
      "id": 2,
      "ts": 20
    }
  ],
  "actions": [
    {
      "op": "page",
      "after": null,
      "limit": 1
    },
    {
      "op": "insert",
      "record": {
        "id": 3,
        "ts": 15
      }
    },
    {
      "op": "page",
      "after": [
        10,
        1
      ],
      "limit": 1
    }
  ]
}
```
Return:
```json
[
  {
    "ids": [
      1
    ],
    "next": [
      10,
      1
    ]
  },
  {
    "ids": [
      3
    ],
    "next": [
      15,
      3
    ]
  }
]
```

## Constraints

- 0–200 initial rows and 0–200 actions. At most 400 rows in total.
- Ids are 1–1000000; timestamps are 0–1000000. All are integers. Limits are 1–50.
- No deletions or timestamp changes. No snapshot isolation or network calls.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 30 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://www.postgresql.org/docs/current/queries-order.html)
- [Official documentation 2](https://www.postgresql.org/docs/current/queries-limit.html)
