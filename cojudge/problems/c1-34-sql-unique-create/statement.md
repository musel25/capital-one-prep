# 34. Create accounts with stable conflict rules

[Course list](/?course=capital-one-engineering-50) · Level 4 · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 24 and 31–33; replay semantics, SQLite placeholders, and queries.

A unique database constraint is the final guard against duplicate keys. Checking for a row in application code before inserting it is not enough when concurrent writers exist. An insert can instead use a conflict policy tied to the unique key. This exercise keeps the first stored value. The application then distinguishes a matching repeated request from a request that tries to change that value. Use bound parameters even when the schema is small. Quotes and SQL punctuation can appear in a valid username. The simulation is sequential, so it demonstrates the constraint and result policy without claiming to test concurrent transactions or durable storage.

</details>

**Scenario:** A sign-up API creates accounts with a unique username. Clients can send the same request again. A repeat with the same data is fine (200). A request that reuses a name with different data is a conflict (409).

Complete `create_account(connection, username, quota)` in the SQLite scaffold. The table has `username TEXT PRIMARY KEY NOT NULL` and `quota INTEGER NOT NULL`. Text comparison is case-sensitive (the default).

**Input:** `data` has:
- `initial`: a list of `{"username": string, "quota": int}`, with unique usernames.
- `requests`: a list of records with the same shape. Usernames can repeat.

**Rules:** for each request:
- New username → insert the row and return `{"status": 201, "record": stored row}`.
- Existing username, same quota → status 200.
- Existing username, different quota → status 409.
- In both existing cases, do not change the row, and return its original record.

**Return:** the scaffold returns `{"responses": [...], "accounts": [...]}`, with the responses in request order and the final accounts in username order.

**Practice:** use a parameterized insert with a uniqueness conflict policy, and a parameterized lookup. The reference runs SQLite. The judge cannot check SQL use or parameter binding.

**Constraints:**

- 0–200 initial accounts and 0–300 requests. Initial usernames are unique with exact case.
- Usernames have 1–80 printable ASCII characters; quotes, spaces, and SQL punctuation are valid.
- Quota is an integer from 0 through 1000000. All records contain exactly username and quota.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 31 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.sqlite.org/lang_upsert.html), [2](https://docs.python.org/3.11/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries)
