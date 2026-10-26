# 02. Parse money into exact cents

[Back to the course list](/?course=capital-one-engineering-50)

**Level 1 · Easy · About 20 minutes**

**Before this problem:** Lists, dictionaries, and functions.

## Learn first

Binary floating point cannot represent many decimal fractions exactly. Money from a text boundary is easier to handle with Decimal. First validate the allowed text format. Then construct Decimal from that text, multiply by 100, and convert the exact result to an integer. This order keeps the cents. Constructing Decimal from a float would preserve the float error. Format validation is a separate concern: Decimal accepts forms that an API might forbid, such as an exponent. This task permits one or two fractional digits and rejects every other text format. Once parsed, integer cents support exact addition and comparison.

## Your task

`data.amounts` is a list of JSON values. A valid amount is a string that fully matches ASCII `-?[0-9]{1,12}(?:\.[0-9]{1,2})?`. It has at most 12 digits before the decimal point. Leading zeros and negative zero are valid. Spaces, a leading plus, exponent notation, Unicode digits, and all non-string values are invalid. Return `{"cents": [...]}` in input order. Each valid amount becomes exact integer cents. Each invalid amount becomes null. Inputs have at most 30 characters.

## Examples

### Example 1: exact decimal conversion

Input to `solve`:
```json
{
  "amounts": [
    "12.34",
    "-0.05",
    "7"
  ]
}
```
Return:
```json
{
  "cents": [
    1234,
    -5,
    700
  ]
}
```

### Example 2: invalid forms

Input to `solve`:
```json
{
  "amounts": [
    "1.234",
    " 2.00",
    2
  ]
}
```
Return:
```json
{
  "cents": [
    null,
    null,
    null
  ]
}
```

### Example 3: empty input

Input to `solve`:
```json
{
  "amounts": []
}
```
Return:
```json
{
  "cents": []
}
```

## Constraints

- At most 100 input items. All input values follow the stated contract.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 27 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3/library/decimal.html)
- [Official documentation 2](https://docs.python.org/3/library/re.html#re.fullmatch)
