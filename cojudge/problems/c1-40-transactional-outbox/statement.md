# 40. Write an order and its outbox event atomically

[Course list](/?course=capital-one-engineering-50) · Level 4 · Hard · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** SQL transactions, primary keys, and idempotent requests.

A business write and a message publish cannot normally share a local database transaction. A transactional outbox stores the intended event beside the business record instead. One database transaction inserts both rows. A separate worker can later publish committed outbox rows and retry delivery. This task covers the producer boundary only. A failure after either insert must leave neither row behind. A repeated order ID with the same amount must not create another event. A repeated ID with a different amount is a conflict. Atomic outbox insertion prevents missing event records, but it does not itself guarantee exactly one delivery to consumers.

</details>

**Scenario:** When an order is saved, other services must hear about it through an event. If the order is saved but the event is lost, or the reverse, the systems disagree. The outbox pattern writes the order and its event in one transaction.

**Input:** `data` has:
- `orders`: an ordered list of `{"id": ..., "amount": ..., "fail": ...}`. `fail` is `"none"`, `"business"` (a fault after the order insert), or `"event"` (a fault after the outbox insert).

**Rules:** for each order:
- **ID already committed:** return `replay` if the amount is the same, or `conflict` if it is different. Do not evaluate `fail`.
- **New ID:** insert the order row and the outbox row in one SQLite transaction. On either fault, roll back and return `failed`. Otherwise commit and return `ok`.

**Return** `{"results": [...], "orders": [[id, amount], ...], "events": [[id, amount], ...]}`. Sort both tables by ASCII ID.

Use the supplied schema. There is no publisher and no network call. The judge cannot check SQL use.

**Constraints:**

- 0–200 orders. IDs are nonempty ASCII strings of length at most 30.
- Amounts are integer minor units from 1 to 1000000.
- The trace is sequential; it does not test real concurrent transactions.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 36 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.sqlite.org/lang_transaction.html), [2](https://docs.python.org/3.11/library/sqlite3.html)
