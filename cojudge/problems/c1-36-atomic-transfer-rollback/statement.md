# 36. Repair an atomic SQL transfer

[Course list](/?course=capital-one-engineering-50) · Level 4 · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** SQL UPDATE, parameterized statements, and Python exceptions.

A transfer changes two balances. Both changes must commit, or neither change must remain. A transaction groups these writes into one unit. Commit only after the debit and credit succeed. Roll back if an exception occurs between them. A conditional debit can check the available balance and subtract the amount in one statement. Its affected-row count tells you whether the debit occurred. Setup writes also need a commit before you start an explicit transaction. This exercise injects a failure after the debit. The starter catches that failure but commits the partial transfer. Repair that transaction boundary and preserve earlier successful transfers.

</details>

**Scenario:** A bank moves money between accounts in a SQLite database. A transfer is a debit plus a credit. If something fails between them, the database must look as if the transfer never started. Operations report that money disappears after failures.

**Bug fix.** Repair the faulty `solve(data)` implementation.

**Input:** `data` has:
- `balances`: maps account IDs to initial integer balances.
- `transfers`: an ordered list of `{"from": ..., "to": ..., "amount": ..., "fail": ...}`. `amount` is positive and `fail` is a boolean. Both IDs exist and differ.

**Rules:** each transfer has its own transaction.
1. If the source has less than `amount` → `insufficient`.
2. Otherwise debit the source.
3. If `fail` is true → roll back and return `failed`.
4. Otherwise credit the destination, commit, and return `ok`.

**Return** `{"results": [...], "balances": {...}}`: one status per transfer, and the final balances.

Use the supplied in-memory SQLite setup. The judge cannot check SQL use.

**Constraints:**

- 0–100 accounts and 0–200 transfers.
- IDs are nonempty ASCII strings. Initial balances are 0–1000000; amounts are 1–1000000.
- Failures are injected exceptions, not actual concurrent operations.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 36 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/sqlite3.html), [2](https://www.sqlite.org/lang_transaction.html)
