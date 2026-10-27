# 16. Model explicit order transitions

[Course list](/?course=capital-one-engineering-50) · Level 2 · Easy · About 20 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Classes, dictionaries, and stateful operations.

A state machine lists which actions are valid in each state. It separates the current state from the events that request a change. A transition table makes the allowed paths easy to inspect. An action that has no transition must leave the state unchanged. This matters when events repeat or arrive in the wrong order. Do not assume that every event moves the process forward. Terminal states may have no valid outgoing actions. This exercise models one order with a small set of named states. It uses a boolean result for each request so a caller can see exactly which requests were accepted.

</details>

**Input:** `data` has:
- `actions`: a list of strings. Each is `authorize`, `capture`, `cancel`, or `refund`.

**Rules:** the order starts in `NEW`. Only these transitions are allowed:

| State | Action | New state |
| --- | --- | --- |
| NEW | authorize | AUTHORIZED |
| NEW | cancel | CANCELLED |
| AUTHORIZED | capture | CAPTURED |
| AUTHORIZED | cancel | CANCELLED |
| CAPTURED | refund | REFUNDED |

Any other action is rejected (`false`) and does not change the state. `CANCELLED` and `REFUNDED` are final states.

**Return** `{"accepted": [bool], "state": string}`: one boolean per action, and the final state.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)
