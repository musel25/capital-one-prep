# 20. Build a typed in-memory ledger

[Course list](/?course=capital-one-engineering-50) · Level 2 · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 11–19: object state, invariants, atomic changes, and event IDs.

A small ledger combines several rules that must agree. Account objects hold balances. A ledger object coordinates transfers so one debit and one credit form a complete operation. A TypedDict describes the transfer input, while immutable tuples record event payloads for duplicate checks. The event ID policy must also define failed requests. In this task, the first request reserves its ID even if it has insufficient funds. Retrying it cannot later turn the same ID into a different operation. A new ID is required for a new attempt. Keep duplicate detection before balance changes and check funds before either side of a transfer changes.

</details>

**Input:** `data` has:
- `accounts`: maps account IDs to nonnegative integer cents.
- `events`: a list of `{"id": string, "from": account_id, "to": account_id, "cents": int}`, with nonnegative `cents`. Both accounts exist.

**Rules:** process the events in order.
- **New ID:** store its payload `(from, to, cents)`. If the source has enough funds, transfer the cents and return `applied`. Otherwise return `insufficient` and change no balances. The ID stays stored after either result.
- **Known ID, same payload:** return `duplicate`.
- **Known ID, different payload:** return `conflict`.
- `duplicate` and `conflict` do not change balances or the stored payload.
- A self-transfer checks funds, then leaves the balances unchanged.

**Return** `{"status": [string], "balances": {...}}`: one status per event, and the final account map.

**Practice:** use typed objects and composition. The judge checks only the output.

**Constraints:**

- At most 30 accounts and 100 events. Initial balances and event cents are at most 1,000,000,000,000. Input objects follow the stated types; runtime boundary validation is outside this task.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 25 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/typing.html#typing.TypedDict), [2](https://docs.python.org/3.11/library/dataclasses.html)
