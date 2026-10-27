# 39. Isolate failed import rows with savepoints

[Course list](/?course=capital-one-engineering-50) · Level 4 · Hard · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Transactions, constraint failures, and exception handling.

A savepoint marks a position inside a transaction. ROLLBACK TO restores that position without discarding earlier work in the transaction. RELEASE removes the savepoint. It does not make inner changes durable when an outer transaction is still open. This is useful for batch imports: one bad row can fail while other rows remain eligible to commit. The final batch decision still controls all accepted rows. A row can also fail after its insert succeeds. In that case the savepoint must remove that inserted row before the next item runs. Keep row outcomes separate from the final batch commit decision.

</details>

**Input:** `data` has:
- `batches`: an ordered list of `{"rows": [...], "abort": bool}`. Each row is `{"id": ..., "qty": ..., "fail": ...}`.

**Rules:** use the supplied SQLite table.
- Each batch is one outer transaction. Attempt each row inside its own savepoint.
- A duplicate ID or a negative `qty` → `invalid`. This check comes before `fail`.
- Otherwise insert the row. If `fail` is true, undo that insert and return `failed`. Otherwise return `ok`.
- Continue with the next row after every row failure.
- At the end of the batch: if `abort` is true, roll back the whole batch. Otherwise commit it.

Row statuses describe each attempt, even if the batch is rolled back later.

**Return** `{"batches": [{"rows": [status, ...], "committed": bool}, ...], "rows": [[id, qty], ...]}`. Sort the final `rows` by ASCII ID.

The judge cannot check SQL use.

**Constraints:**

- 0–30 batches, each with 0–30 rows.
- IDs are nonempty ASCII strings. Quantities are -100–1000000. fail and abort are Boolean.
- No actual concurrent transactions occur.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 37 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.sqlite.org/lang_savepoint.html), [2](https://docs.python.org/3.11/library/sqlite3.html)
