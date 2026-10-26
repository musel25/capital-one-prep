# 22. Validate a request body

[Back to the course list](/?course=capital-one-engineering-50)

**Level 3 · Easy · About 25 minutes**

**Before this problem:** Problem 21; strict Python type checks and regular expressions.

## Learn first

A JSON parser can accept a value that your API cannot use. Validation is a separate boundary. First check the whole body shape. Then check required fields, types, ranges, and unknown keys. Do not silently turn a string into a number unless the contract permits that conversion. Python needs care because bool is a subclass of int. Error ordering is part of this exercise's contract, so clients can compare responses reliably. The status choices below are a local API policy, not a claim that every service uses the same validation convention. A successful result includes explicit defaults for optional fields.

## Your task

`data.bodies` is a list of decoded JSON values. Return one response per body. A non-object body returns `{status:400, errors:["body"]}`. An object allows only `account`, `amount`, and optional `note`. `account` is required and must fully match `[a-z][a-z0-9_]{0,11}`. `amount` is required and must be a JSON integer from 1 through 10000, excluding booleans and floats. For example, `1` is an integer token but `1.0` and `1e0` are not. `note` defaults to null and must be null or an ASCII string of at most 20 characters. On invalid fields return status 422 with `errors` in this exact order: account, amount, note, unknown. Include only failed checks. Use one `unknown` entry if any unknown key exists. Otherwise return `{status:201, body:{account:..., amount:..., note:...}}`. Do not include errors in a success response. Do not trim or coerce input.

## Examples

### Example 1: valid body gets default null note

Input to `solve`:
```json
{
  "bodies": [
    {
      "account": "acct_1",
      "amount": 25
    }
  ]
}
```
Return:
```json
[
  {
    "status": 201,
    "body": {
      "account": "acct_1",
      "amount": 25,
      "note": null
    }
  }
]
```

### Example 2: all field errors have fixed order

Input to `solve`:
```json
{
  "bodies": [
    {
      "account": "A",
      "amount": 0,
      "note": false,
      "extra": 1
    }
  ]
}
```
Return:
```json
[
  {
    "status": 422,
    "errors": [
      "account",
      "amount",
      "note",
      "unknown"
    ]
  }
]
```

### Example 3: JSON null is not an object

Input to `solve`:
```json
{
  "bodies": [
    null
  ]
}
```
Return:
```json
[
  {
    "status": 400,
    "errors": [
      "body"
    ]
  }
]
```

## Constraints

- 0–200 bodies. Every string and object key is ASCII and at most 100 characters.
- Numeric inputs are finite JSON numbers in [-100000,100000]. Decimal or exponent notation decodes as float and must fail the amount check.
- Bodies and field values may have any JSON type. Nested lists and objects have at most 10 elements.

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

- [Official documentation 1](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)
- [Official documentation 2](https://www.rfc-editor.org/rfc/rfc9110.html)
