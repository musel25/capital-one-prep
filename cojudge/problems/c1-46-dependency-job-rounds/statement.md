# 46. Schedule dependent jobs and detect blocked cycles

[Back to the course list](/?course=capital-one-engineering-50)

**Level 5 · Hard · About 35 minutes**

**Before this problem:** Sets, directed graphs, and dependency order.

## Learn first

A job is ready when every prerequisite has completed. A dependency scheduler can repeatedly select ready jobs, run a bounded batch, and then mark that batch complete. All jobs in this task take one round, so a job cannot start in the same round as its prerequisite. If unfinished jobs remain but none is ready, the remaining dependency graph contains a cycle. Some blocked jobs may only depend on a cycle and are not themselves part of it. Report all unfinished jobs separately from the cycle flag. A fixed tie rule makes results reproducible. This is a deterministic event trace model, not an actual parallel, thread, or network test.

## Your task

`jobs` contains objects with unique ASCII `id` and `depends`, a list of distinct existing job IDs. `workers` is the maximum jobs per round. At the start of each round, find every unfinished job whose dependencies completed in earlier rounds. Select up to `workers` in ascending ASCII ID order. All selected jobs complete at the end of that round. Stop when all jobs finish or no job is ready. Return `{rounds: [[id, ...], ...], blocked: [...], has_cycle: Boolean}`. Sort blocked IDs. `has_cycle` is true exactly when jobs remain blocked. Self dependencies and cycles are valid inputs. Do not claim every blocked job belongs to a cycle.

## Examples

### Example 1: dependencies finish before next round

Input to `solve`:
```json
{
  "jobs": [
    {
      "id": "a",
      "depends": []
    },
    {
      "id": "b",
      "depends": [
        "a"
      ]
    },
    {
      "id": "c",
      "depends": [
        "a"
      ]
    }
  ],
  "workers": 2
}
```
Return:
```json
{
  "rounds": [
    [
      "a"
    ],
    [
      "b",
      "c"
    ]
  ],
  "blocked": [],
  "has_cycle": false
}
```

### Example 2: worker limit and ASCII tie break

Input to `solve`:
```json
{
  "jobs": [
    {
      "id": "c",
      "depends": []
    },
    {
      "id": "b",
      "depends": []
    },
    {
      "id": "a",
      "depends": []
    }
  ],
  "workers": 2
}
```
Return:
```json
{
  "rounds": [
    [
      "a",
      "b"
    ],
    [
      "c"
    ]
  ],
  "blocked": [],
  "has_cycle": false
}
```

### Example 3: cycle blocks both jobs

Input to `solve`:
```json
{
  "jobs": [
    {
      "id": "a",
      "depends": [
        "b"
      ]
    },
    {
      "id": "b",
      "depends": [
        "a"
      ]
    }
  ],
  "workers": 2
}
```
Return:
```json
{
  "rounds": [],
  "blocked": [
    "a",
    "b"
  ],
  "has_cycle": true
}
```

## Constraints

- 0–100 jobs, at most 100 dependencies per job, and 1–20 workers.
- Every dependency refers to a supplied job. Each job takes exactly one round and always succeeds.

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

- [Official documentation 1](https://docs.python.org/3.11/library/graphlib.html)
