# 04. Sort tickets with stable ties

[Back to the course list](/?course=capital-one-engineering-50)

**Level 1 · Easy · About 20 minutes**

**Before this problem:** Lists, dictionaries, and functions.

## Learn first

A sort key can express several business rules. Python compares tuples from left to right. Negating an integer makes a larger value sort first while the next key can still sort in ascending order. Python sorting is stable: records with equal keys keep their original relative order. Stability is useful when input order is the final tie rule. Do not add an identifier as a tie breaker unless the contract asks for it. Two valid ordering choices can produce different results for the same records. Use sorted when you want a new list and want to preserve the caller’s input.

## Your task

`data.tickets` is a list of objects with string `id`, integer `priority` from 0 through 9, and integer `created` from 0 through 1,000,000. Return a list of IDs. Order by priority descending, then created ascending. If both fields tie, keep input order. IDs need not be unique. ID text never changes the order.

## Examples

### Example 1: two ordering keys

Input to `solve`:
```json
{
  "tickets": [
    {
      "id": "low",
      "priority": 1,
      "created": 1
    },
    {
      "id": "late",
      "priority": 3,
      "created": 9
    },
    {
      "id": "early",
      "priority": 3,
      "created": 2
    }
  ]
}
```
Return:
```json
[
  "early",
  "late",
  "low"
]
```

### Example 2: ties preserve input order

Input to `solve`:
```json
{
  "tickets": [
    {
      "id": "z",
      "priority": 2,
      "created": 5
    },
    {
      "id": "a",
      "priority": 2,
      "created": 5
    }
  ]
}
```
Return:
```json
[
  "z",
  "a"
]
```

### Example 3: empty list

Input to `solve`:
```json
{
  "tickets": []
}
```
Return:
```json
[]
```

## Constraints

- At most 1,000 tickets. All records contain the required fields.

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

- [Official documentation 1](https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts)
