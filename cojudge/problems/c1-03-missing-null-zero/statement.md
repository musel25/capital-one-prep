# 03. Keep missing, null, and zero separate

[Back to the course list](/?course=capital-one-engineering-50)

**Level 1 · Easy · About 20 minutes**

**Before this problem:** Lists, dictionaries, and functions.

## Learn first

A field can be absent, present with null, or present with zero. These states often have different meanings. Dictionary membership tells you whether a key exists. A value of None represents JSON null after decoding. Zero is a configured numeric value, even though it is false in a boolean condition. An expression such as value or default merges these states and can replace a valid zero. Write the decision in the same order as the contract: first check membership, then inspect the stored value. This makes defaults explicit and avoids an accidental change to a caller’s configuration.

## Your task

`data` has nonnegative integer `default` and a list `records`. Each record is an object. It may contain `limit`, whose value is a nonnegative integer or null. Ignore other keys. An absent `limit` resolves to `default`. An explicit null resolves to null. Zero stays zero. Return `{"limits": [resolved_values], "configured": count}`. Count only records that contain a non-null `limit`, including zero.

## Examples

### Example 1: three distinct field states

Input to `solve`:
```json
{
  "default": 10,
  "records": [
    {},
    {
      "limit": null
    },
    {
      "limit": 0
    },
    {
      "limit": 4
    }
  ]
}
```
Return:
```json
{
  "limits": [
    10,
    null,
    0,
    4
  ],
  "configured": 2
}
```

### Example 2: count records, not distinct values

Input to `solve`:
```json
{
  "default": 5,
  "records": [
    {
      "limit": 2
    },
    {
      "limit": 2
    }
  ]
}
```
Return:
```json
{
  "limits": [
    2,
    2
  ],
  "configured": 2
}
```

### Example 3: empty records

Input to `solve`:
```json
{
  "default": 9,
  "records": []
}
```
Return:
```json
{
  "limits": [],
  "configured": 0
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

- [Official documentation 1](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict)
