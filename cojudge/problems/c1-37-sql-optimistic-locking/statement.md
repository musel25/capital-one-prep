# 37. Reject stale SQL updates

[Course list](/?course=capital-one-engineering-50) · Level 4 · Medium · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** SQL UPDATE and transaction basics.

A client can read a document and then write after another client has changed it. A version number lets the database detect that stale write. The client sends the version it read. One UPDATE statement checks that version, changes the value, and increments the version. If the statement changes no rows, the client must refresh its data before it retries. Checking the version in a separate read is not the same guarantee: another writer could run between the read and write. This exercise supplies an ordered trace of client proposals. Even a write of the same value counts as an accepted update and advances the version.

</details>

**Input:** `data` has:
- `value`: the initial document string.
- `version`: its initial integer version.
- `updates`: a list of `{"value": string, "expected": int}`.

**Rules:** for each update:
- Accept it only when `expected` is equal to the current version. Then replace the value and add 1 to the version.
- A rejected update changes nothing.

**Return** `{"accepted": [bool], "value": string, "version": int}`.

Complete the SQL update loop in the scaffold. This is a sequential trace, not a test of real parallel execution. The judge cannot check SQL syntax or structure.

**Constraints:**

- 0–200 updates. Versions and expected versions are 0–1000000.
- Values are ASCII strings of length 0–100.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 36 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.sqlite.org/lang_update.html), [2](https://docs.python.org/3.11/library/sqlite3.html)
