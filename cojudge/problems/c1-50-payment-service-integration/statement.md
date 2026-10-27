# 50. Compose a bounded reliable payment service

[Course list](/?course=capital-one-engineering-50) · Level 5 · Hard · About 45 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Atomic transfers, idempotency payloads, and transactional outbox records.

A reliable payment boundary combines rules that are easy to implement incorrectly in isolation. The idempotency key identifies the complete request payload, including both accounts and the amount. A successful payment changes two balances, records that key, and creates an event as one logical commit. Replays return before checking the current balance because the original payment already happened. Failed attempts retain no key, so they can retry after recovery. This bounded exercise stages changes in memory and publishes them only after all fault points pass. It is a deterministic event trace, not an actual parallel, thread, or network test. Production storage would need a real durable transaction.

</details>

**Input:** `data` has:
- `balances`: maps existing account IDs to nonnegative integer balances.
- `payments`: a list of `{"key": ..., "from": ..., "to": ..., "amount": ..., "fail": ...}`. The two accounts exist and differ. `amount` is positive. `fail` is `"none"`, `"debit"` (a fault after the debit is staged), or `"outbox"` (a fault after the event is prepared).

**Rules:** for each payment:
1. **Key already committed:** the same `(from, to, amount)` → `"replay"`. Any difference → `"conflict"`. These checks ignore `fail` and the current funds.
2. **New key, and the source has less than `amount`:** return `"insufficient"`. Do not store the key.
3. **New key otherwise:** stage the debit, the credit, the key, and the outbox event as one atomic operation.
   - Either fault → return `"failed"`. No committed state changes, and the key is not reserved.
   - No fault → commit and return `"ok"`.

**Return** `{"results": [...], "balances": {...}, "events": [[key, from, to, amount], ...]}`. Events are in successful commit order. No network delivery is needed.

**Constraints:**

- 0–100 accounts and 0–300 payments. IDs and keys are nonempty ASCII strings.
- Initial balances are 0–1000000 and amounts are 1–1000000.
- Implement only this bounded state model; no HTTP server, database setup, or background worker is required.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 39 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.sqlite.org/lang_transaction.html), [2](https://docs.python.org/3.11/library/copy.html)
