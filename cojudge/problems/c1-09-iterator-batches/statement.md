# 09. Keep the final iterator batch

[Back to the course list](/?course=capital-one-engineering-50)

**Level 1 · Easy · About 20 minutes**

**Before this problem:** Lists, dictionaries, and functions.

## Learn first

An iterator gives values one at a time and remembers its current position. You can group its values without indexing the original sequence. itertools.islice reads up to a fixed number of values from the current iterator position. The final group can be shorter than the requested batch size. That partial group still contains work and must be emitted. Stop only when a read returns no values. In a real streaming application, this pattern can limit the active buffer to one batch. This exercise returns every batch as JSON, so the complete result still occupies memory. The grouping logic should preserve every item exactly once.

## Your task

`data` has `values`, a list of integers from -1,000,000 through 1,000,000, and `size`, an integer from 1 through 20. Return consecutive batches as a list of lists. Each batch has `size` items except a possible final nonempty partial batch. Preserve order and duplicates. An empty input returns an empty list. Use an iterator and itertools.islice for practice; the judge checks the grouping behavior.

## Examples

### Example 1: final partial batch

Input to `solve`:
```json
{
  "values": [
    1,
    2,
    3,
    4,
    5
  ],
  "size": 2
}
```
Return:
```json
[
  [
    1,
    2
  ],
  [
    3,
    4
  ],
  [
    5
  ]
]
```

### Example 2: exact multiple

Input to `solve`:
```json
{
  "values": [
    7,
    8,
    9,
    10
  ],
  "size": 2
}
```
Return:
```json
[
  [
    7,
    8
  ],
  [
    9,
    10
  ]
]
```

### Example 3: empty iterator

Input to `solve`:
```json
{
  "values": [],
  "size": 3
}
```
Return:
```json
[]
```

## Constraints

- At most 100 input items. All input values follow the stated contract.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 24 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3.11/library/itertools.html#itertools.islice)
