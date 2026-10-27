# 07. Check accepted and rejected state transitions

[Course list](/?course=capital-one-codebase-practice) · Level 2 · Easy · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 05–06. Read a sequence of operations that updates object state.

The program stores one order state and a table of allowed transitions. The starter permits an operation that the contract rejects. Your objective is to check the table against the product rule and preserve state when an action is rejected.

A state machine lists which actions are valid in each state. It separates the current state from the events that request a change. A transition table makes the allowed paths easy to inspect. An action that has no transition must leave the state unchanged. This matters when events repeat or arrive in the wrong order. Do not assume that every event moves the process forward. Terminal states may have no valid outgoing actions. This exercise models one order with a small set of named states. It uses a boolean result for each request so a caller can see exactly which requests were accepted.

</details>

**Scenario:** An online store tracks the payment of each order with a state machine. An order is authorized, then captured (the money is taken), then maybe refunded. It can be cancelled only before capture. `solve` processes the actions that arrive and reports which ones were valid.

> **Bug report:** "My order was already captured, so my card was charged. Then a cancel came in, and the system accepted it. The order now says CANCELLED, but I never got my money back."

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

**What to fix:** The starter runs, but it has one intentional bug.

- Repair the allowed transition definition.
- Keep the five contract transitions and no others.
- Preserve the initial state, output flags, terminal states, and action order.
- Do not make a rejected action reset the order or count as success.
- Do not introduce cancellation or refund rules beyond this constructed model.

**Constraints:**

- At most 100 input items. All input values follow the stated contract.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Trace actions `["capture", "authorize", "capture", "authorize", "refund"]`. The first action fails in `NEW`. Authorization moves to `AUTHORIZED`; capture moves to `CAPTURED`. Repeated authorization fails and leaves `CAPTURED`. Refund then reaches `REFUNDED`. Expect accepted flags `[false, true, true, false, true]`. The later refund also confirms that the preceding rejection preserved state.

### Read the existing code

Inspect `Order.TRANSITIONS` as data, not just code. Compare each `(state, action)` pair with the stated transition list. Follow `Order.apply` through lookup, rejection, and assignment. Finally inspect the list comprehension in `solve`, which applies actions sequentially to one `Order`.

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

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 24 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 08](/problems/cb-08-atomic-memory-batch).

Official documentation: [1](https://docs.python.org/3.11/library/stdtypes.html#mapping-types-dict)
