# 06. Trace a composed fee dependency

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 2 · Medium · About 35 minutes**

**Before this problem:** Exercise 05. Follow an object method call and read an integer calculation.

## Learn first

The calculator receives a policy object and calls its `fee` method. The rate policy has a rounding defect. Your objective is to separate dependency selection, fee calculation, and result construction, then repair only the responsible layer.

Composition gives an object another object that performs part of its work. A small protocol describes the methods that the dependency must provide. Python Protocol supports structural typing: a class can satisfy the interface without explicitly inheriting from it. A calculator can depend on fee(amount) instead of checking policy types for every amount. Select the policy once at the boundary, then let the calculator call it. This is polymorphism through a shared interface. Integer arithmetic can also make a percentage fee exact. To round a nonnegative integer fraction upward, add denominator minus one before integer division.

### Worked trace

Select a rate policy of `125` basis points and amounts `[0, 80, 81]`. The exact unrounded fees are `0`, `1`, and `1.0125` cents. Round each upward to obtain fees `[0, 1, 2]` and totals `[0, 81, 83]`. `solve` selects the policy once. Each `Calculator.quote` delegates one amount to that policy and adds the returned fee.

### Read the existing code

Inspect the `FeePolicy.fee` signature. Follow construction in `solve` to `Calculator.__init__` and `Calculator.quote`. Compare `FlatFee.fee` and `RateFee.fee`. Identify which layer knows the policy kind and which layer knows how a quote is represented. Check units: amounts and fees are cents; `bps` is a rate.

## Your task

### Scoped repair

Repair the integer calculation in `RateFee.fee`. Keep the Protocol interface, constructor inputs, and quote shape. Preserve `FlatFee` behavior, including a flat charge for amount zero. Do not add policy-type branches to `Calculator.quote`. Keep exact integer arithmetic and the input amount unchanged.

### Required behavior

`data.policy` is either `{"kind":"flat","cents":nonnegative_integer}` or `{"kind":"rate","bps":integer_from_0_to_10000}`. `data.amounts` is a list of nonnegative integer cent amounts. One basis point is 1/100 of one percent. Flat fee equals `cents`, including for amount zero. Rate fee is amount × bps / 10000, rounded upward to whole cents. Return a list of `{"fee": integer, "total": amount_plus_fee}` in input order. Practice Protocol and composition; the judge checks outputs only.

### Test before and after the change

Before Run, compute a rate fee with a zero remainder and one with a nonzero remainder. Use `bps = 125` with amounts `80` and `81` as a pair. Also test amount zero, rate zero, rate `10000`, and a one-cent amount at a small positive rate. Test a nonzero flat fee on amount zero as a compatibility check. Assert both `fee` and `total`; a correct total shape can still contain the wrong fee.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “A zero amount must always have a zero fee, regardless of the selected policy.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py`. Explain how `Calculator` uses `FeePolicy` without selecting a concrete policy on every quote. Cite the selection, storage, delegation, and output lines. Identify the units in the rate calculation. Do not give a rounding expression, implementation, or test code. I will derive the arithmetic cases.

### Technical completion checks

- Map the dependency from policy selection to quote output.
- Run exact-division, fractional-cent, and flat-policy cases.
- Review integer arithmetic and delegation. The judge does not inspect Protocol use or dependency design.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 07](/problems/cb-07-explicit-order-states).

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
