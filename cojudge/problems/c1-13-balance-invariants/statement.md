# 13. Keep an account balance nonnegative

[Back to the course list](/?course=capital-one-engineering-50)

**Level 2 · Easy · About 20 minutes**

**Before this problem:** Classes, methods, and integer cents.

## Learn first

An invariant is a rule that must hold after every operation. Here the balance must never become negative. Put balance changes inside account methods so the rule has one enforcement point. A property can expose the current balance without providing a public setter. A leading underscore marks an internal attribute by Python convention; it is not a security barrier. Check a withdrawal before changing state. If it fails, the method should return a failure result and leave the balance unchanged. Keeping this rule in the object makes the calling loop simple and gives future operations a clear place to enforce the same invariant.

## Your task

`data.balance` is a nonnegative integer number of cents. `data.actions` contains `{"op":"deposit"|"withdraw","cents":nonnegative_integer}`. A deposit always succeeds. A withdrawal succeeds exactly when cents is at most the current balance. A failed withdrawal changes nothing. Zero-cent actions succeed. Return `{"accepted": [booleans], "balance": final_integer}` with one boolean per action. Implement an Account class with controlled balance updates for practice; the output judge checks the invariant’s visible behavior.

## Examples

### Example 1: failed withdrawal preserves balance

Input to `solve`:
```json
{
  "balance": 10,
  "actions": [
    {
      "op": "withdraw",
      "cents": 7
    },
    {
      "op": "withdraw",
      "cents": 4
    }
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
  "balance": 3
}
```

### Example 2: deposit then exact withdrawal

Input to `solve`:
```json
{
  "balance": 0,
  "actions": [
    {
      "op": "deposit",
      "cents": 5
    },
    {
      "op": "withdraw",
      "cents": 5
    }
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

### Example 3: no actions

Input to `solve`:
```json
{
  "balance": 9,
  "actions": []
}
```
Return:
```json
{
  "accepted": [],
  "balance": 9
}
```

## Constraints

- At most 100 actions. Initial balance and action cents are at most 1,000,000,000,000.

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

- [Official documentation 1](https://docs.python.org/3.11/tutorial/classes.html#private-variables)
- [Official documentation 2](https://docs.python.org/3.11/library/functions.html#property)
