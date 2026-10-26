# 14. Extend an account with a fee rule

[Back to the course list](/?course=capital-one-engineering-50)

**Level 2 · Medium · About 25 minutes**

**Before this problem:** Classes and the balance invariant exercise.

## Learn first

Inheritance lets a subclass reuse a base implementation while replacing a specific behavior. A subclass initializer can call super().__init__ to establish the base state before adding its own fields. A base method can call another instance method such as withdrawal_fee. Python then selects the override on the actual object. This keeps the withdrawal check in one place while allowing a premium account to use a different fee rule. Avoid copying the whole withdrawal method just to change one calculation. Both amount and fee must fit in the balance. A rejected operation must charge neither of them.

## Your task

`data` contains `kind` (`standard` or `premium`), nonnegative integer `balance`, nonnegative integer `fee`, nonnegative integer `threshold`, and a list of positive integer `withdrawals`. All amounts use cents. Standard accounts charge `fee` on every successful withdrawal. Premium accounts charge zero fee when the requested withdrawal is at least `threshold`; otherwise they charge `fee`. A withdrawal succeeds when amount plus applicable fee is at most the current balance. Failure changes nothing. Return `{"accepted": [booleans], "balance": final_integer}`. Practice inheritance, super(), and a fee-method override. The judge checks behavior, not class structure.

## Examples

### Example 1: fee is part of the funds check

Input to `solve`:
```json
{
  "kind": "standard",
  "balance": 20,
  "fee": 2,
  "threshold": 10,
  "withdrawals": [
    10,
    8
  ]
}
```
Return:
```json
{
  "accepted": [
    true,
    false
  ],
  "balance": 8
}
```

### Example 2: premium fee override

Input to `solve`:
```json
{
  "kind": "premium",
  "balance": 20,
  "fee": 2,
  "threshold": 10,
  "withdrawals": [
    10,
    8
  ]
}
```
Return:
```json
{
  "accepted": [
    true,
    true
  ],
  "balance": 0
}
```

### Example 3: no withdrawals

Input to `solve`:
```json
{
  "kind": "premium",
  "balance": 10,
  "fee": 3,
  "threshold": 10,
  "withdrawals": []
}
```
Return:
```json
{
  "accepted": [],
  "balance": 10
}
```

## Constraints

- At most 100 withdrawals. Numeric input values are at most 1,000,000,000,000.

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

- [Official documentation 1](https://docs.python.org/3.11/tutorial/classes.html#inheritance)
- [Official documentation 2](https://docs.python.org/3.11/library/functions.html#super)
