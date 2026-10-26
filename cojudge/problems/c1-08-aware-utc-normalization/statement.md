# 08. Normalize aware timestamps to UTC

[Back to the course list](/?course=capital-one-engineering-50)

**Level 1 · Easy · About 20 minutes**

**Before this problem:** Lists, dictionaries, and functions.

## Learn first

An aware datetime has a time zone offset. It identifies an instant rather than an unqualified wall-clock reading. To express that instant in another time zone, use astimezone. Replacing tzinfo changes the label without adjusting the clock and usually changes the instant. An offset conversion can move the date to the previous or next day. Fixed offsets already contain the information needed for this task. They do not require local time zone rules. Parse each timestamp, convert it to UTC, and format all outputs in one consistent form. Preserve the input order because normalization does not imply sorting.

## Your task

`data.timestamps` is a list of valid strings in `YYYY-MM-DDTHH:MM:SSZ` or `YYYY-MM-DDTHH:MM:SS±HH:MM` form. Input years are 2000 through 2099. Offsets range from -14:00 through +14:00. Dates and clock fields are valid, with no leap seconds or fractional seconds. Each timestamp includes an offset; local names such as America/Tijuana do not occur. Return the same instants, in input order, as `YYYY-MM-DDTHH:MM:SSZ` strings. A UTC date outside the input year range is valid.

## Examples

### Example 1: same instant from two offsets

Input to `solve`:
```json
{
  "timestamps": [
    "2026-10-26T09:30:00-07:00",
    "2026-10-26T16:30:00Z"
  ]
}
```
Return:
```json
[
  "2026-10-26T16:30:00Z",
  "2026-10-26T16:30:00Z"
]
```

### Example 2: previous day and year

Input to `solve`:
```json
{
  "timestamps": [
    "2026-01-01T00:15:00+02:00"
  ]
}
```
Return:
```json
[
  "2025-12-31T22:15:00Z"
]
```

### Example 3: empty list

Input to `solve`:
```json
{
  "timestamps": []
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

Use **Run** for the three examples. Use **Submit** for all 25 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.python.org/3.11/library/datetime.html#datetime.datetime.astimezone)
