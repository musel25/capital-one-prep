# 07. Check accepted and rejected state transitions

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 2 · Easy · About 30 minutes**

**Before this problem:** Exercises 05–06. Read a sequence of operations that updates object state.

## Learn first

The program stores one order state and a table of allowed transitions. The starter permits an operation that the contract rejects. Your objective is to check the table against the product rule and preserve state when an action is rejected.

A state machine lists which actions are valid in each state. It separates the current state from the events that request a change. A transition table makes the allowed paths easy to inspect. An action that has no transition must leave the state unchanged. This matters when events repeat or arrive in the wrong order. Do not assume that every event moves the process forward. Terminal states may have no valid outgoing actions. This exercise models one order with a small set of named states. It uses a boolean result for each request so a caller can see exactly which requests were accepted.

### Worked trace

Trace actions `["capture", "authorize", "capture", "authorize", "refund"]`. The first action fails in `NEW`. Authorization moves to `AUTHORIZED`; capture moves to `CAPTURED`. Repeated authorization fails and leaves `CAPTURED`. Refund then reaches `REFUNDED`. Expect accepted flags `[false, true, true, false, true]`. The later refund also confirms that the preceding rejection preserved state.

### Read the existing code

Inspect `Order.TRANSITIONS` as data, not just code. Compare each `(state, action)` pair with the stated transition list. Follow `Order.apply` through lookup, rejection, and assignment. Finally inspect the list comprehension in `solve`, which applies actions sequentially to one `Order`.

## Your task

### Scoped repair

Repair the allowed transition definition. Keep the five contract transitions and no others. Preserve the initial state, output flags, terminal states, and action order. Do not make a rejected action reset the order or count as success. Do not introduce cancellation or refund rules beyond this constructed model.

### Required behavior

An order starts in `NEW`. `data.actions` is a list containing only `authorize`, `capture`, `cancel`, or `refund`. Allowed transitions are: NEW + authorize → AUTHORIZED; NEW + cancel → CANCELLED; AUTHORIZED + capture → CAPTURED; AUTHORIZED + cancel → CANCELLED; CAPTURED + refund → REFUNDED. No other transition is allowed. An invalid action returns false and leaves the current state unchanged. Return `{"accepted": [booleans], "state": final_state}`. CANCELLED and REFUNDED are terminal states.

### Test before and after the change

Build your own table of allowed and rejected state/action pairs. Use valid action prefixes to reach each state. Before Run, predict `["authorize", "capture", "cancel", "refund"]`, including the state after each action. Test repeated authorization, capture before authorization, cancellation from both allowed states, and every action after a terminal state. Assert the flags as well as the final state; equal final states can hide a wrongly accepted request.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “Repeating an accepted authorization should return true because the desired authorized state was already reached.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py` and my state/action table. Compare the table with `Order.TRANSITIONS` and the control flow in `Order.apply`. Cite file lines for acceptance, rejection, and state assignment. Point out assumptions I should verify. Do not edit the transition table or write an implementation.

### Technical completion checks

- Compare every transition entry with the stated rule.
- Run a rejection followed by a valid action to test preserved state.
- Review the transition table and accepted flags. Passing cases do not prove coverage of every sequence.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 08](/problems/cb-08-atomic-memory-batch).

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
