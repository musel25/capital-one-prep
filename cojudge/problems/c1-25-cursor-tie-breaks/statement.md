# 25. Page by timestamp and id

[Course list](/?course=capital-one-engineering-50) · Level 3 · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 21–24; tuple ordering and state changes.

Offset pagination counts how many rows to skip. An insertion before that position can shift later pages. A cursor can instead store the final ordering key from the previous page. The next query asks for keys strictly after that key. A timestamp alone is not sufficient when records share a timestamp. Add a unique id to create a total order. This exercise makes the cursor visible as a pair so the ordering rule is easy to inspect. New records after the cursor can appear in later results. Records inserted before it will not appear there. Cursor pagination alone does not create a database snapshot.

</details>

**Input:** `data` has:
- `records`: a list of `{"id": int, "ts": int}`.
- `actions`: a list of operations:
  - `{"op": "insert", "record": {"id": int, "ts": int}}` adds a record. IDs are unique across all records.
  - `{"op": "page", "after": null | [ts, id], "limit": int}` requests one page.

**Rules for each page**
1. Take the current records, sorted by `(ts, id)` ascending.
2. If `after` is not null, keep only the records whose `(ts, id)` is strictly greater than `after`. The cursor does not have to match an existing record.
3. Take at most `limit` records.
4. Set `next` to the `[ts, id]` of the last record taken, but only if more eligible records remain. Otherwise `next` is `null`, also for an empty page.

Each page uses only its own `after` cursor.

**Return** a list with one `{"ids": [...], "next": ...}` per page operation. Inserts add nothing to the output.

**Constraints:**

- 0–200 initial rows and 0–200 actions. At most 400 rows in total.
- Ids are 1–1000000; timestamps are 0–1000000. All are integers. Limits are 1–50.
- No deletions or timestamp changes. No snapshot isolation or network calls.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 30 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.postgresql.org/docs/current/queries-order.html), [2](https://www.postgresql.org/docs/current/queries-limit.html)
