# 13. Test the boundary of a composite cursor

[Course list](/?course=capital-one-codebase-practice) · Level 4 · Medium · About 45 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 09–12 and local labs 05–06. Read tuple ordering and page cursors.

A page request filters current records by a two-part ordering key. The starter includes a boundary record that should be excluded. Your objective is to separate eligibility, ordering, selection, and continuation before repairing the filter.

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

**What to fix:** The starter runs, but it has one intentional bug.

- Repair cursor eligibility.
- Preserve the complete pair order and exclude the cursor boundary itself.
- Keep insert order irrelevant to sorted results.
- Keep `next` only when more eligible records remain.
- Do not require the cursor to name an existing record.
- Do not add remembered cursor state, offset pagination, or snapshot behavior.
- Limits start at 1 under the contract.

**Constraints:**

- 0–200 initial rows and 0–200 actions. At most 400 rows in total.
- Ids are 1–1000000; timestamps are 0–1000000. All are integers. Limits are 1–50.
- No deletions or timestamp changes. No snapshot isolation or network calls.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Use records `(id 8, ts 6)`, `(id 3, ts 6)`, and `(id 2, ts 7)`. A page after `[6, 3]` with limit `1` selects id `8` and returns next `[6, 8]`, because id `2` remains eligible. A page after `[6, 8]` selects id `2` and returns null next. A full page is not sufficient evidence that another page exists.

### Read the existing code

Inspect `records` and the insert branch in `solve`. Follow the generator that builds `eligible`, its sort key, the `selected` slice, `more`, and `cursor`. Write the ordering key as `(ts, id)` at each stage. Confirm that each page reads its own supplied `after` value instead of an implicit cursor from the preceding action.

### Test before and after the change

Before Run, predict a page whose timestamp equals the cursor timestamp but whose IDs lie below, at, and above the cursor ID. Use unsorted input. Test zero eligible rows, exactly `limit` eligible rows, and `limit + 1` eligible rows. Use a cursor absent from the records. Between page requests, insert one row before the cursor and one after it. Assert both selected IDs and `next`. A repeated boundary row can hide if a test only checks page length.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “Whenever a page contains exactly the requested number of records, it must return a non-null next cursor.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py` and my hand-ordered record table. Trace the table through `eligible`, `selected`, `more`, and `cursor`. Cite file lines for each stage. Review the cursor and insertion assumptions in my cases. Do not provide a filter expression, implementation, or tests.

### Technical completion checks

- Write the composite order and page boundary expectations by hand.
- Run equality, absent-cursor, page-size, and insertion cases.
- Review continuation semantics. These checks do not establish database snapshot consistency or query performance.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 30 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 14](/problems/cb-14-retry-backoff).

Official documentation: [1](https://www.postgresql.org/docs/current/queries-order.html), [2](https://www.postgresql.org/docs/current/queries-limit.html)
