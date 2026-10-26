# 15. Compose a calculator with a fee policy

[Back to the course list](/?course=capital-one-engineering-50)

**Level 2 · Medium · About 25 minutes**

**Before this problem:** Classes, type annotations, and integer arithmetic.

## Learn first

Composition gives an object another object that performs part of its work. A small protocol describes the methods that the dependency must provide. Python Protocol supports structural typing: a class can satisfy the interface without explicitly inheriting from it. A calculator can depend on fee(amount) instead of checking policy types for every amount. Select the policy once at the boundary, then let the calculator call it. This is polymorphism through a shared interface. Integer arithmetic can also make a percentage fee exact. To round a nonnegative integer fraction upward, add denominator minus one before integer division.

## Your task

`data.policy` is either `{"kind":"flat","cents":nonnegative_integer}` or `{"kind":"rate","bps":integer_from_0_to_10000}`. `data.amounts` is a list of nonnegative integer cent amounts. One basis point is 1/100 of one percent. Flat fee equals `cents`, including for amount zero. Rate fee is amount × bps / 10000, rounded upward to whole cents. Return a list of `{"fee": integer, "total": amount_plus_fee}` in input order. Practice Protocol and composition; the judge checks outputs only.

## Examples

### Example 1: flat fee includes zero amount

Input to `solve`:
```json
{
  "policy": {
    "kind": "flat",
    "cents": 3
  },
  "amounts": [
    0,
    10
  ]
}
```
Return:
```json
[
  {
    "fee": 3,
    "total": 3
  },
  {
    "fee": 3,
    "total": 13
  }
]
```

### Example 2: rate fees round upward

Input to `solve`:
```json
{
  "policy": {
    "kind": "rate",
    "bps": 250
  },
  "amounts": [
    100,
    200,
    1
  ]
}
```
Return:
```json
[
  {
    "fee": 3,
    "total": 103
  },
  {
    "fee": 5,
    "total": 205
  },
  {
    "fee": 1,
    "total": 2
  }
]
```

### Example 3: no quotes

Input to `solve`:
```json
{
  "policy": {
    "kind": "rate",
    "bps": 10
  },
  "amounts": []
}
```
Return:
```json
[]
```

## Constraints

- At most 100 amounts. Cent values are at most 1,000,000,000,000.

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

- [Official documentation 1](https://docs.python.org/3.11/library/typing.html#typing.Protocol)
