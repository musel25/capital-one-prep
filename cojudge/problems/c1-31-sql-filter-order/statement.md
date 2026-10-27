# 31. Query posted transfers safely

[Course list](/?course=capital-one-engineering-50) · Level 4 · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 1–30; Python functions and API input boundaries. No prior SQL is required.

SQL describes the rows you want from a table. SELECT chooses output columns. WHERE keeps rows that meet a condition. ORDER BY defines their result order, and LIMIT bounds the number returned. Without a complete ordering rule, equal values can appear in an unstable order. Add a unique id as a tie breaker. Python's sqlite3 module passes query values separately through placeholders. A name containing a quote must remain a value rather than become part of SQL text. The supplied code creates an in-memory database and loads the input. Your task is to write the selection query, not database setup code.

</details>

**Scenario:** A banking dashboard lists a customer's largest posted transfers. Customer names come from user input and can contain quotes, so the query must use bound parameters, not string formatting.

Complete `select_rows(connection, owner, minimum, limit)` in the supplied SQLite scaffold.

**Input:** `data` has:
- `rows`: a list of `{"id": int, "owner": string, "amount": int, "posted": bool}`, with unique ids. The scaffold loads them into `transfers(id, owner, amount, posted)`, with `posted` stored as 0 or 1.
- `owner`, `minimum`, `limit`: the query parameters.

**Rules:** select the rows where:
- `owner` is exactly equal to the given owner,
- `posted` is 1, and
- `amount` is at least `minimum`.

Order by `amount` descending, then `id` ascending. Take at most `limit` rows.

**Return** a list of `{"id": int, "amount": int}`. The scaffold turns your query rows into this list.

**Practice:** use bound parameters for `owner`, `minimum`, and `limit`. The reference runs real SQLite queries. The judge checks only the output. It cannot check SQL use or parameter binding.

**Constraints:**

- 0–300 rows; ids are 1–1000000. amount and minimum are integers in [-1000000,1000000].
- limit is 0–100. Owner strings have 1–80 printable ASCII characters, including possible quotes and SQL punctuation.
- All input rows meet the schema; there are no duplicate ids or null fields.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 32 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.python.org/3.11/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries), [2](https://www.sqlite.org/lang_select.html)
