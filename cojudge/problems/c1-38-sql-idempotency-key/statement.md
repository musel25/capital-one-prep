# 38. Commit a credit and its idempotency key

[Course list](/?course=capital-one-engineering-50) · Level 4 · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Transactions, UNIQUE constraints, and request retries.

A retry can arrive after the first request has already committed. An idempotency key identifies that logical request. Store the key and its payload in a table with a uniqueness constraint. A repeat with the same payload returns a replay result. A repeat with a different payload is a conflict. The key and the business write must share one transaction. Otherwise a crash can record the key without applying the credit, or apply the credit without recording the key. A failed transaction leaves the key available for a later attempt. This task models ordered requests and an injected failure immediately before commit.

</details>

**Scenario:** A wallet service adds credits to an account. Clients retry requests, so each credit has a key. The key and the balance change must be saved in the same transaction. Otherwise a crash could save one without the other.

**Input:** `data` has:
- `balance`: the initial account balance.
- `credits`: a list of `{"key": ..., "amount": ..., "fail": ...}`.

**Rules:** for each credit, in order:
- **Key already committed:** return `replay` if the amount is the same, or `conflict` if it is different. Nothing changes. This check comes before `fail`.
- **New key:** in one transaction, insert the key and add the amount. If `fail` is true, roll back both writes and return `failed`. Otherwise commit and return `ok`.

**Return** `{"results": [...], "balance": int, "keys": [...]}`. `keys` lists the committed keys in ASCII order.

Use the supplied SQLite tables. The judge cannot check SQL use.

**Constraints:**

- 0–200 credits. Balance is 0–1000000; amounts are 1–1000000.
- Keys are nonempty ASCII strings of length at most 30. fail is Boolean.
- This ordered trace does not test actual parallel transactions.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 36 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.sqlite.org/lang_createtable.html), [2](https://docs.python.org/3.11/library/sqlite3.html)
