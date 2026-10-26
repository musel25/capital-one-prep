# 07. Validate JSON before using TypedDict

[Back to the course list](/?course=capital-one-engineering-50)

**Level 1 · Easy · About 20 minutes**

**Before this problem:** Lists, dictionaries, and functions.

## Learn first

TypedDict describes the expected keys and value types in a dictionary for a static type checker. It does not validate a decoded JSON value at runtime. A value from json.loads can still be a list, a number, or an object with missing fields. Put a validator at the boundary. Check the outer type before you read keys. Check each required field and then build a small accepted object. That object can have a TypedDict return annotation because the function has established its shape. Extra fields need a stated policy. This task ignores them and returns only the validated fields.

## Your task

`data.records` is a list of arbitrary JSON values. Accept a record if it is an object with a nonempty string `id` and a nonnegative integer `amount`. Booleans and floats are not integers for this rule. Integers have absolute value at most 1,000,000. Ignore extra keys. Return `{"valid": [{"id": string, "amount": integer}], "rejected": [zero_based_positions]}`. The valid list contains only the two required fields, in input order. The rejected list also follows input order. Use TypedDict in your solution for practice; the output judge checks behavior only.

## Examples

### Example 1: validate fields at the boundary

Input to `solve`:
```json
{
  "records": [
    {
      "id": "A",
      "amount": 0
    },
    {
      "id": "B",
      "amount": true
    },
    {
      "id": "C"
    }
  ]
}
```
Return:
```json
{
  "valid": [
    {
      "id": "A",
      "amount": 0
    }
  ],
  "rejected": [
    1,
    2
  ]
}
```

### Example 2: drop extra fields

Input to `solve`:
```json
{
  "records": [
    {
      "id": "X",
      "amount": 4,
      "debug": true
    }
  ]
}
```
Return:
```json
{
  "valid": [
    {
      "id": "X",
      "amount": 4
    }
  ],
  "rejected": []
}
```

### Example 3: empty list

Input to `solve`:
```json
{
  "records": []
}
```
Return:
```json
{
  "valid": [],
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

- [Official documentation 1](https://docs.python.org/3.11/library/typing.html#typing.TypedDict)
