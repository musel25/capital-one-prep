# 01. Strict numeric fields

[Back to the course list](/?course=capital-one-engineering-50)

**Level 1 · Easy · About 20 minutes**

**Before this problem:** Lists, dictionaries, and functions.

## Learn first

Python treats bool as a subclass of int. As a result, isinstance(True, int) returns True. This can turn a flag into one cent when you validate a numeric field. At a JSON boundary, decide which exact types the contract permits. Use type(value) is int when a field requires an integer and must exclude booleans. Validate the range in a separate condition. Do not convert strings or round floats unless the contract requires it. Keep rejected positions so a caller can identify each bad field. Zero is a valid amount in this task. An empty batch has a total of zero.

## Your task

`data` has `values`, a list of JSON values. Accept a value only when its exact Python type is `int` and it is at least zero. JSON integers have absolute value at most 1,000,000,000. Reject booleans, floats, strings, null, lists, objects, and negative integers. Return `{"total": sum_of_accepted_values, "rejected": [zero_based_positions]}`. Keep rejected positions in input order.

## Examples

### Example 1: flags and text are not amounts

Input to `solve`:
```json
{
  "values": [
    7,
    true,
    0,
    -2,
    "4"
  ]
}
```
Return:
```json
{
  "total": 7,
  "rejected": [
    1,
    3,
    4
  ]
}
```

### Example 2: all amounts are valid

Input to `solve`:
```json
{
  "values": [
    2,
    3,
    5
  ]
}
```
Return:
```json
{
  "total": 10,
  "rejected": []
}
```

### Example 3: empty batch

Input to `solve`:
```json
{
  "values": []
}
```
Return:
```json
{
  "total": 0,
  "rejected": []
}
```

## Constraints

- At most 100 input items. All input values follow the stated contract.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 25 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)
