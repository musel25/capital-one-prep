# 48. Preserve read-your-writes with version floors

[Back to the course list](/?course=capital-one-engineering-50)

**Level 5 · Medium · About 30 minutes**

**Before this problem:** Version numbers, replication lag, and deterministic selection.

## Learn first

Replicas can lag behind a completed write. A client can carry the version of its last write as a minimum acceptable version for later reads. A replica below that floor must not answer the read, even if it is reachable. If none qualifies, the caller must wait or use another source. This exercise selects the freshest eligible replica and uses its ID to break ties. Replication updates can also arrive out of order, so a replica must never replace a newer version with an older one. All equal versions represent the same value here. This is a deterministic event trace, not an actual parallel, thread, or network test.

## Your task

`replicas` contains unique `{id, version, value}` records. `ops` contains `publish` with an existing `id`, `version`, and `value`, or `read` with `min_version`. Publish a higher version and return `applied`; ignore a lower version and return `stale`; an equal version returns `unchanged`. For a read, eligible replicas have version at least min_version. Return `{id, version, value}` for the highest version, breaking ties by smallest ASCII ID, or null if none qualifies. Return `{results: [...], replicas: [[id, version, value], ...]}` with final replicas sorted by ID. A read's min_version is the supplied client write token; do not infer it from other reads. Across all input records and publications, equal versions always have equal values.

## Examples

### Example 1: choose freshest eligible replica

Input to `solve`:
```json
{
  "replicas": [
    {
      "id": "a",
      "version": 1,
      "value": 10
    },
    {
      "id": "b",
      "version": 3,
      "value": 30
    }
  ],
  "ops": [
    {
      "op": "read",
      "min_version": 2
    }
  ]
}
```
Return:
```json
{
  "results": [
    {
      "id": "b",
      "version": 3,
      "value": 30
    }
  ],
  "replicas": [
    [
      "a",
      1,
      10
    ],
    [
      "b",
      3,
      30
    ]
  ]
}
```

### Example 2: stale replica cannot satisfy read token

Input to `solve`:
```json
{
  "replicas": [
    {
      "id": "a",
      "version": 1,
      "value": 10
    }
  ],
  "ops": [
    {
      "op": "read",
      "min_version": 2
    }
  ]
}
```
Return:
```json
{
  "results": [
    null
  ],
  "replicas": [
    [
      "a",
      1,
      10
    ]
  ]
}
```

### Example 3: equal version tie uses ASCII ID

Input to `solve`:
```json
{
  "replicas": [
    {
      "id": "b",
      "version": 2,
      "value": 20
    },
    {
      "id": "a",
      "version": 2,
      "value": 20
    }
  ],
  "ops": [
    {
      "op": "read",
      "min_version": 2
    }
  ]
}
```
Return:
```json
{
  "results": [
    {
      "id": "a",
      "version": 2,
      "value": 20
    }
  ],
  "replicas": [
    [
      "a",
      2,
      20
    ],
    [
      "b",
      2,
      20
    ]
  ]
}
```

## Constraints

- 0–100 replicas and 0–300 operations. Publish IDs always exist.
- IDs are nonempty ASCII strings; versions and min_version are 0–1000000; values are integers from -1000000 to 1000000.

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

- [Official documentation 1](https://learn.microsoft.com/en-us/azure/cosmos-db/consistency-levels)
