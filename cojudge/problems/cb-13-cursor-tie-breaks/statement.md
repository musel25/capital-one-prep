# 13. Test the boundary of a composite cursor

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 4 · Medium · About 45 minutes**

**Before this problem:** Exercises 09–12 and local labs 05–06. Read tuple ordering and page cursors.

## Learn first

A page request filters current records by a two-part ordering key. The starter includes a boundary record that should be excluded. Your objective is to separate eligibility, ordering, selection, and continuation before repairing the filter.

Offset pagination counts how many rows to skip. An insertion before that position can shift later pages. A cursor can instead store the final ordering key from the previous page. The next query asks for keys strictly after that key. A timestamp alone is not sufficient when records share a timestamp. Add a unique id to create a total order. This exercise makes the cursor visible as a pair so the ordering rule is easy to inspect. New records after the cursor can appear in later results. Records inserted before it will not appear there. Cursor pagination alone does not create a database snapshot.

### Worked trace

Use records `(id 8, ts 6)`, `(id 3, ts 6)`, and `(id 2, ts 7)`. A page after `[6, 3]` with limit `1` selects id `8` and returns next `[6, 8]`, because id `2` remains eligible. A page after `[6, 8]` selects id `2` and returns null next. A full page is not sufficient evidence that another page exists.

### Read the existing code

Inspect `records` and the insert branch in `solve`. Follow the generator that builds `eligible`, its sort key, the `selected` slice, `more`, and `cursor`. Write the ordering key as `(ts, id)` at each stage. Confirm that each page reads its own supplied `after` value instead of an implicit cursor from the preceding action.

## Your task

### Scoped repair

Repair cursor eligibility. Preserve the complete pair order and exclude the cursor boundary itself. Keep insert order irrelevant to sorted results. Keep `next` only when more eligible records remain. Do not require the cursor to name an existing record. Do not add remembered cursor state, offset pagination, or snapshot behavior. Limits start at 1 under the contract.

### Required behavior

`records` is a list of `{id:int, ts:int}`. `actions` contains inserts `{op:"insert", record:{id,ts}}` and page requests `{op:"page", after:null|[ts,id], limit:int}`. Inserted ids are globally unique. For each page, use current records ordered by ascending `(ts,id)`. If after is non-null, keep only keys strictly greater than it. Take at most limit records. Return `{ids:[...], next:cursor}` for that page. Set next to the final selected `[ts,id]` only if more eligible records remain. Otherwise next is null, including an empty page. A cursor need not name an existing record. Return only page responses; inserts produce none. Each page uses its supplied cursor independently.

### Test before and after the change

Before Run, predict a page whose timestamp equals the cursor timestamp but whose IDs lie below, at, and above the cursor ID. Use unsorted input. Test zero eligible rows, exactly `limit` eligible rows, and `limit + 1` eligible rows. Use a cursor absent from the records. Between page requests, insert one row before the cursor and one after it. Assert both selected IDs and `next`. A repeated boundary row can hide if a test only checks page length.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “Whenever a page contains exactly the requested number of records, it must return a non-null next cursor.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py` and my hand-ordered record table. Trace the table through `eligible`, `selected`, `more`, and `cursor`. Cite file lines for each stage. Review the cursor and insertion assumptions in my cases. Do not provide a filter expression, implementation, or tests.

### Technical completion checks

- Write the composite order and page boundary expectations by hand.
- Run equality, absent-cursor, page-size, and insertion cases.
- Review continuation semantics. These checks do not establish database snapshot consistency or query performance.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 14](/problems/cb-14-retry-backoff).

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
