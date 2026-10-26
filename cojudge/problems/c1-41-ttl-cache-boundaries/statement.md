# 41. Expire and invalidate cache entries

[Back to the course list](/?course=capital-one-engineering-50)

**Level 5 · Medium · About 25 minutes**

**Before this problem:** Dictionaries and integer time arithmetic.

## Learn first

A time-to-live cache stores a value and its expiration time. If an entry is written at time t with lifetime d, its expiration is t + d. It is usable only while the current time is strictly less than that expiration. Reads do not extend this lifetime unless the contract explicitly says so. An overwrite replaces both the value and its expiration. Invalidation removes the entry immediately. Distinguish a missing key from a cached value such as zero. This exercise uses an integer clock supplied by each operation. It is a deterministic event trace, not an actual parallel, thread, or network test.

## Your task

`ops` contains operations with nondecreasing integer `at` times. Before every operation, remove all entries whose expiration is at or before `at`. `put` has `key`, integer `value`, and `ttl`; replace the entry and return `stored`. A zero TTL removes any old entry and stores nothing. `get` has `key`; return its value or null if absent. `invalidate` has `key`; return true if an unexpired entry was removed, otherwise false. Return `{results: [...], keys: [...]}`, with one result per operation and remaining keys sorted in ASCII order after the last operation. An empty trace returns empty lists.

## Examples

### Example 1: read before expiration

Input to `solve`:
```json
{
  "ops": [
    {
      "op": "put",
      "at": 0,
      "key": "a",
      "value": 7,
      "ttl": 5
    },
    {
      "op": "get",
      "at": 4,
      "key": "a"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "stored",
    7
  ],
  "keys": [
    "a"
  ]
}
```

### Example 2: exact expiration is a miss

Input to `solve`:
```json
{
  "ops": [
    {
      "op": "put",
      "at": 0,
      "key": "a",
      "value": 7,
      "ttl": 5
    },
    {
      "op": "get",
      "at": 5,
      "key": "a"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "stored",
    null
  ],
  "keys": []
}
```

### Example 3: explicit invalidation

Input to `solve`:
```json
{
  "ops": [
    {
      "op": "put",
      "at": 0,
      "key": "a",
      "value": 7,
      "ttl": 5
    },
    {
      "op": "invalidate",
      "at": 1,
      "key": "a"
    },
    {
      "op": "get",
      "at": 2,
      "key": "a"
    }
  ]
}
```
Return:
```json
{
  "results": [
    "stored",
    true,
    null
  ],
  "keys": []
}
```

## Constraints

- 0–300 operations. at and ttl are 0–1000000.
- Keys are nonempty ASCII strings; values are integers from -1000000 to 1000000.

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

- [Official documentation 1](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)
