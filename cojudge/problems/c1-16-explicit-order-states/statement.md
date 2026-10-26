# 16. Model explicit order transitions

[Back to the course list](/?course=capital-one-engineering-50)

**Level 2 · Easy · About 20 minutes**

**Before this problem:** Classes, dictionaries, and stateful operations.

## Learn first

A state machine lists which actions are valid in each state. It separates the current state from the events that request a change. A transition table makes the allowed paths easy to inspect. An action that has no transition must leave the state unchanged. This matters when events repeat or arrive in the wrong order. Do not assume that every event moves the process forward. Terminal states may have no valid outgoing actions. This exercise models one order with a small set of named states. It uses a boolean result for each request so a caller can see exactly which requests were accepted.

## Your task

An order starts in `NEW`. `data.actions` is a list containing only `authorize`, `capture`, `cancel`, or `refund`. Allowed transitions are: NEW + authorize → AUTHORIZED; NEW + cancel → CANCELLED; AUTHORIZED + capture → CAPTURED; AUTHORIZED + cancel → CANCELLED; CAPTURED + refund → REFUNDED. No other transition is allowed. An invalid action returns false and leaves the current state unchanged. Return `{"accepted": [booleans], "state": final_state}`. CANCELLED and REFUNDED are terminal states.

## Examples

### Example 1: complete valid path

Input to `solve`:
```json
{
  "actions": [
    "authorize",
    "capture",
    "refund"
  ]
}
```
Return:
```json
{
  "accepted": [
    true,
    true,
    true
  ],
  "state": "REFUNDED"
}
```

### Example 2: invalid order and repeated action

Input to `solve`:
```json
{
  "actions": [
    "capture",
    "authorize",
    "authorize",
    "capture"
  ]
}
```
Return:
```json
{
  "accepted": [
    false,
    true,
    false,
    true
  ],
  "state": "CAPTURED"
}
```

### Example 3: no events

Input to `solve`:
```json
{
  "actions": []
}
```
Return:
```json
{
  "accepted": [],
  "state": "NEW"
}
```

## Constraints

- At most 100 input items. All input values follow the stated contract.

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

- [Official documentation 1](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)
