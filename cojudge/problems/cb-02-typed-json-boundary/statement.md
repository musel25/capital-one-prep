# 02. Find the runtime validation boundary

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 1 · Easy · About 30 minutes**

**Before this problem:** Exercise 01. Read dictionary keys, return values, and rejection paths.

## Learn first

This program separates one-record validation from batch processing. `validate` returns an accepted `Entry` or `None`; `solve` records the result. The starter accepts a value that the amount rule excludes. Your objective is to locate the runtime check that must enforce the rule.

TypedDict describes the expected keys and value types in a dictionary for a static type checker. It does not validate a decoded JSON value at runtime. A value from json.loads can still be a list, a number, or an object with missing fields. Put a validator at the boundary. Check the outer type before you read keys. Check each required field and then build a small accepted object. That object can have a TypedDict return annotation because the function has established its shape. Extra fields need a stated policy. This task ignores them and returns only the validated fields.

### Worked trace

Trace records `[7, {"id": "Q", "amount": 0, "debug": true}, {"id": "R", "amount": 1.0}]`. Position `0` fails the outer shape check. Position `1` becomes `{"id": "Q", "amount": 0}`; the extra field is absent from the result. Position `2` fails the amount type rule. Thus `valid` has one entry and `rejected` is `[0, 2]`. The annotation does not make these decisions.

### Read the existing code

Inspect the `Entry` declaration, the return paths in `validate`, and the `enumerate` loop in `solve`. Find where the outer object shape is checked before `.get` is used. Find where a new accepted dictionary is built. Distinguish a rejected position from an accepted record's `id`.

## Your task

### Scoped repair

Repair the amount acceptance check in `validate`. Keep the `Entry` model and the caller's `None` convention. Do not coerce strings or floats. Preserve zero, valid duplicate IDs, and any nonempty ID string. Keep only the two accepted fields. Do not add trimming or ID uniqueness rules.

### Required behavior

`data.records` is a list of arbitrary JSON values. Accept a record if it is an object with a nonempty string `id` and a nonnegative integer `amount`. Booleans and floats are not integers for this rule. Integers have absolute value at most 1,000,000. Ignore extra keys. Return `{"valid": [{"id": string, "amount": integer}], "rejected": [zero_based_positions]}`. The valid list contains only the two required fields, in input order. The rejected list also follows input order. Use TypedDict in your solution for practice; the output judge checks behavior only.

### Test before and after the change

Make a table for amounts `0`, `-1`, `true`, `false`, `1.0`, `"1"`, null, and an absent amount. Predict acceptance before Run. Use a valid ID in these cases so one rule is under test. Separately test a non-object, an empty ID, a space-only ID, and extra keys. Place a valid record between two invalid records to check the original rejection positions.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “A string containing only one space is an invalid ID, because an ID must contain visible text.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py`, including `Entry`, `validate`, and `solve`. Explain which checks establish an `Entry` at runtime. Cite file lines for each rejection path and the accepted-object construction. Identify assumptions made by the caller. Do not write a validator, a repair, or tests. I will write the boundary cases.

### Technical completion checks

- Write an acceptance table before changing validate.
- Run cases that distinguish integers, booleans, and floats.
- Review the Entry construction and rejection positions. Judge results do not prove correct use of TypedDict.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 03](/problems/cb-03-dataclass-list-isolation).

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
