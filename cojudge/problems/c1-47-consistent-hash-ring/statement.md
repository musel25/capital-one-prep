# 47. Route requests around a consistent hash ring

[Back to the course list](/?course=capital-one-engineering-50)

**Level 5 · Hard · About 30 minutes**

**Before this problem:** Sorted lists, binary search, and dictionaries.

## Learn first

A hash ring assigns each request to the first node at or after its hash, moving in increasing hash order. If no node remains in that direction, the search wraps to the first node. An exact hash match belongs to that node. Adding a node changes the interval immediately before it; removing a node hands its interval to its successor. This exercise supplies deterministic integer hashes so that language hash randomization cannot change the answers. Python's bisect_left finds the required insertion position, including exact matches. The model uses one point per node. This is a deterministic event trace, not an actual parallel, thread, or network test.

## Your task

`nodes` contains `{id, hash}` with unique IDs and hash values. Hashes lie on a ring from 0 through 999. Process `ops` in order. `lookup` has `hash`: return the ID at the smallest active hash greater than or equal to it; wrap to the smallest hash if necessary; return null for an empty ring. `add` has a currently unused `id` and `hash`: add it and return `added`. `remove` has `id`: remove it and return true, or return false if absent. Return `{results: [...], ring: [[hash, id], ...]}` with the final ring sorted by hash. Inputs supply hashes directly; do not call Python's hash function.

## Examples

### Example 1: clockwise successor

Input to `solve`:
```json
{
  "nodes": [
    {
      "id": "a",
      "hash": 100
    },
    {
      "id": "b",
      "hash": 500
    }
  ],
  "ops": [
    {
      "op": "lookup",
      "hash": 101
    }
  ]
}
```
Return:
```json
{
  "results": [
    "b"
  ],
  "ring": [
    [
      100,
      "a"
    ],
    [
      500,
      "b"
    ]
  ]
}
```

### Example 2: exact hash belongs to that node

Input to `solve`:
```json
{
  "nodes": [
    {
      "id": "a",
      "hash": 100
    },
    {
      "id": "b",
      "hash": 500
    }
  ],
  "ops": [
    {
      "op": "lookup",
      "hash": 100
    }
  ]
}
```
Return:
```json
{
  "results": [
    "a"
  ],
  "ring": [
    [
      100,
      "a"
    ],
    [
      500,
      "b"
    ]
  ]
}
```

### Example 3: wrap past final point

Input to `solve`:
```json
{
  "nodes": [
    {
      "id": "a",
      "hash": 100
    },
    {
      "id": "b",
      "hash": 500
    }
  ],
  "ops": [
    {
      "op": "lookup",
      "hash": 999
    }
  ]
}
```
Return:
```json
{
  "results": [
    "a"
  ],
  "ring": [
    [
      100,
      "a"
    ],
    [
      500,
      "b"
    ]
  ]
}
```

## Constraints

- 0–100 initial nodes and 0–300 operations. Active hashes and IDs remain unique.
- IDs are nonempty ASCII strings. Removed IDs and hash points may later be reused.

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

- [Official documentation 1](https://docs.python.org/3.11/library/bisect.html)
