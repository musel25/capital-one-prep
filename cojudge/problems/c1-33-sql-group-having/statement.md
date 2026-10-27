# 33. Summarize groups without losing NULL meaning

[Course list](/?course=capital-one-engineering-50) · Level 4 · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 31–32; filtering, NULL, and deterministic output order.

Aggregation combines several rows into one summary. WHERE selects source rows before grouping. HAVING selects completed groups using aggregate values. COUNT(*) counts rows, while COUNT(amount) counts only rows whose amount is not NULL. SUM ignores NULL amounts and returns NULL when every amount in a group is NULL. A report can explicitly replace that result with zero through COALESCE. Equal amounts in different entries are still separate business events. Adding DISTINCT would change their meaning. This exercise asks for both row count and known-value count so that missing amounts remain visible even when the displayed total defaults to zero.

</details>

**Scenario:** A finance team wants a summary of the paid entries of each account: how many there are, how many have a known amount, and the total. Some amounts are unknown (`null`). The report shows only the accounts above the thresholds.

Complete `summary_rows(connection, minimum_total, minimum_events)`. The scaffold loads `rows` into `entries(id PRIMARY KEY, account, amount nullable, kind)`.

**Input:** `data` has `rows`, `minimum_total`, and `minimum_events`.

**Rules**
1. Keep only the rows with kind paid.
2. Group by the exact `account` string. An account with no paid rows does not form a group.
3. For each group, calculate:
   - `events`: the number of paid rows.
   - `valued`: the number of paid rows with a non-null amount.
   - `total`: the sum of the non-null amounts, or 0 if all are null.
4. Keep the groups with `total` at least `minimum_total` and `events` at least `minimum_events`.

**Return** a list of `{"account": ..., "events": ..., "valued": ..., "total": ...}`, ordered by `total` descending, then `account` ascending in SQLite's default binary order.

**Practice:** use SQL aggregation and HAVING with bound thresholds. The reference runs SQLite. The judge cannot check SQL use or the clauses you choose.

**Constraints:**

- 0–300 rows with unique ids from 1 through 1000000.
- account is a nonempty printable ASCII string of at most 40 characters. kind is paid or void.
- amount is null or an integer in [-1000000,1000000]. minimum_total is in [-300000000,300000000]; minimum_events is 1–300.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 32 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.sqlite.org/lang_aggfunc.html), [2](https://www.sqlite.org/lang_select.html#resultset)
