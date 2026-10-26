# 42. Build a capacity-bounded LRU cache

[Back to the course list](/?course=capital-one-engineering-50)

**Level 5 · Medium · About 30 minutes**

**Before this problem:** Dictionaries, ordered collections, and cache misses.

## Learn first

A least-recently-used cache evicts the entry whose last successful use is oldest. A successful read counts as use. In this contract, an insert or overwrite also counts as use. A missing read does not change the order. Python's OrderedDict can move a key to the newest end and remove a key from the oldest end. This keeps the value and recency order in one structure. Capacity is a count of entries, not a byte limit. Capacity zero is still valid: every inserted key is immediately evicted. This exercise is a deterministic event trace, not an actual parallel, thread, or network test.

## Your task

`capacity` is the maximum entry count. `ops` contains `put` with `key` and integer `value`, `get` with `key`, or `delete` with `key`. A put inserts or overwrites and makes the key most recent. If capacity is exceeded, evict the least recent key. Its result is the evicted key, or null if none. A get returns the value and makes the key most recent, or returns null without changing order. A delete returns whether the key existed and removes it. Return `{results: [...], entries: [[key, value], ...]}`. List final entries from least recent to most recent.

## Examples

### Example 1: evict oldest use

Input to `solve`:
```json
{
  "capacity": 2,
  "ops": [
    {
      "op": "put",
      "key": "a",
      "value": 1
    },
    {
      "op": "put",
      "key": "b",
      "value": 2
    },
    {
      "op": "put",
      "key": "c",
      "value": 3
    }
  ]
}
```
Return:
```json
{
  "results": [
    null,
    null,
    "a"
  ],
  "entries": [
    [
      "b",
      2
    ],
    [
      "c",
      3
    ]
  ]
}
```

### Example 2: read refreshes recency

Input to `solve`:
```json
{
  "capacity": 2,
  "ops": [
    {
      "op": "put",
      "key": "a",
      "value": 1
    },
    {
      "op": "put",
      "key": "b",
      "value": 2
    },
    {
      "op": "get",
      "key": "a"
    },
    {
      "op": "put",
      "key": "c",
      "value": 3
    }
  ]
}
```
Return:
```json
{
  "results": [
    null,
    null,
    1,
    "b"
  ],
  "entries": [
    [
      "a",
      1
    ],
    [
      "c",
      3
    ]
  ]
}
```

### Example 3: overwrite refreshes recency

Input to `solve`:
```json
{
  "capacity": 2,
  "ops": [
    {
      "op": "put",
      "key": "a",
      "value": 1
    },
    {
      "op": "put",
      "key": "b",
      "value": 2
    },
    {
      "op": "put",
      "key": "a",
      "value": 9
    }
  ]
}
```
Return:
```json
{
  "results": [
    null,
    null,
    null
  ],
  "entries": [
    [
      "b",
      2
    ],
    [
      "a",
      9
    ]
  ]
}
```

## Constraints

- Capacity is 0–100; there are 0–300 operations.
- Keys are nonempty ASCII strings. Values are integers from -1000000 to 1000000.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 37 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3.11/library/collections.html#collections.OrderedDict)
