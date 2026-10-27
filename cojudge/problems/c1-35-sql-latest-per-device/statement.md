# 35. Select the latest row per device

[Course list](/?course=capital-one-engineering-50) · Level 4 · Hard · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 31–34; SQL ordering, grouping, and NULL values.

Selecting the latest row in each group needs more than finding the maximum timestamp. Several rows can share that timestamp, and the result must keep values from one chosen row. A window function numbers rows within a partition while keeping their other columns. Partition by device and order each partition from newest to oldest. Add a unique id to resolve timestamp ties. Then select the row numbered one. A cutoff belongs before ranking when the question is the latest eligible row. Filtering only after choosing the overall newest row could remove a device that still has older eligible data.

</details>

**Scenario:** An IoT dashboard shows the latest reading of each sensor at a given time (`cutoff`). Readings can arrive out of order.

Complete `latest_rows(connection, cutoff)` in the SQLite scaffold. The table is `readings(id PRIMARY KEY, device, ts, value)`.

**Input:** `data` has:
- `rows`: a list of `{"id": int, "device": string, "ts": int, "value": int | null}`, with unique ids.
- `cutoff`: an integer.

**Rules**
- Use only the rows with `ts` at most `cutoff`.
- For each exact device string, select the row with the greatest `ts`. On a tie, select the greatest `id`.
- Keep the value of that row, even when it is null.
- A device with no eligible rows is not in the output.

**Return** a list of `{"device": ..., "id": ..., "ts": ..., "value": ...}`, ordered by `device` ascending in SQLite's default binary order.

**Practice:** use `ROW_NUMBER` with `PARTITION BY` and a deterministic order. The reference runs a real SQLite window query. The judge cannot check SQL or window-function use.

**Constraints:**

- 0–400 rows. Ids are 1–1000000; ts and cutoff are integers from 0 through 1000000.
- Device names have 1–50 printable ASCII characters and are case sensitive.
- value is null or an integer in [-1000000,1000000]. Input row order has no meaning.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 32 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.sqlite.org/windowfunctions.html), [2](https://docs.python.org/3.11/library/sqlite3.html)
