# 05. Reconcile repeated item IDs

[Back to the course list](/?course=capital-one-engineering-50)

**Level 1 · Easy · About 20 minutes**

**Before this problem:** Lists, dictionaries, and functions.

## Learn first

A set records whether an item is present. It does not record how many times the item occurs. Counter stores a count for each key and acts as a multiset. In a reconciliation task, repeated IDs can represent separate units. Counter subtraction keeps only positive counts. Therefore expected minus observed gives missing units, and observed minus expected gives extra units. Neither result includes zero or negative counts. Keep the input meaning separate from output order. Sorting the result keys makes the report deterministic even when two batches list their units in different orders. The output should preserve counts, not expand each count into repeated rows.

## Your task

`data` has `expected` and `observed`, each a list of strings. Repeated strings count as separate units. Return `{"missing": [{"id": string, "count": positive_integer}], "extra": [...]}`. Missing count is max(expected count minus observed count, 0). Extra count is the reverse difference. Sort each list by ID in ascending ASCII order. IDs contain only ASCII characters. Do not include zero counts.

## Examples

### Example 1: counts in both directions

Input to `solve`:
```json
{
  "expected": [
    "A",
    "A",
    "B"
  ],
  "observed": [
    "A",
    "C"
  ]
}
```
Return:
```json
{
  "missing": [
    {
      "id": "A",
      "count": 1
    },
    {
      "id": "B",
      "count": 1
    }
  ],
  "extra": [
    {
      "id": "C",
      "count": 1
    }
  ]
}
```

### Example 2: order does not matter

Input to `solve`:
```json
{
  "expected": [
    "B",
    "A"
  ],
  "observed": [
    "A",
    "B"
  ]
}
```
Return:
```json
{
  "missing": [],
  "extra": []
}
```

### Example 3: empty batches

Input to `solve`:
```json
{
  "expected": [],
  "observed": []
}
```
Return:
```json
{
  "missing": [],
  "extra": []
}
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

- [Official documentation 1](https://docs.python.org/3/library/collections.html#collections.Counter)
