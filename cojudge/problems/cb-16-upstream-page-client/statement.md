# 16. Review the full path through a paged client

[Course list](/?course=capital-one-codebase-practice) · Level 4 · Hard · About 50 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 13–15. Trace cursor, duplicate, timeout, and error state through one loop.

This final browser task combines traversal, duplicate handling, stop guards, and partial results in one `solve` function. The starter stops before following a valid continuation. Your objective is to repair cursor progression and then review its interactions with every existing guard. The pages are fixtures; no network is used.

A pagination client needs a completion condition and guards against faulty upstream behavior. An empty page can still point to another page. Repeated records need a documented merge rule. A repeated cursor can create an infinite loop unless the client remembers which cursors it already requested. A separate page cap also stops a long chain of distinct cursors. Decide what happens to useful data when a later page fails. This exercise keeps the accepted prefix and reports the failure. The pages are supplied fixtures, so the client makes no network calls. Combining these rules checks control flow that a single happy-path page cannot reveal.

</details>

**Scenario:** Your service downloads a full list from a partner API, page by page, and follows the `next` cursor of each page. The partner API is unreliable: it can loop, fail, or point to pages that do not exist. Your client must stop safely and keep what it already has. `pages` is a recorded copy of the partner's responses.

> **Bug report:** "The partner API returned an empty page that still had a `next` cursor. Our import stopped there and missed all the later items."

**Input:** `data` has:
- `start`: the first cursor.
- `max_pages`: the maximum number of page requests.
- `pages`: an object that maps cursors to page fixtures:
  - Success: `{"status": 200, "items": [{"id": int, "value": string}], "next": string | null}`
  - Error: `{"status": 429 or 500–599}`, with no other fields.

**Rules:** start at `start`. Before each fetch:
1. If this cursor was already requested → stop with error `cycle`.
2. Else if `max_pages` requests were already made → stop with `limit`.
3. Add the cursor to `requests`.
4. No fixture for the cursor → stop with `missing`. An error page → stop with `upstream`.
5. A success page: append each item whose `id` was not seen before. Keep the first value of an id. Then follow `next`, also after an empty `items` list. A `null` next ends with no error.

Keep the items collected before an error. Do not retry. Ignore fixtures that are never reached.

**Return** `{"items": [...], "requests": [cursors], "error": null | "cycle" | "limit" | "missing" | "upstream"}`.

**What to fix:** The starter runs, but it has one intentional bug.

- Repair continuation after a successful page.
- Preserve cycle-before-limit priority, attempted-request recording, first-value-wins deduplication, and accepted items on failure.
- Keep null next as completion.
- Do not treat an empty item list as an error.
- Do not add retries or change the meaning of the cap.
- Keep unreachable fixtures irrelevant.

**Constraints:**

- 1–20 max_pages; 0–30 page fixtures; 0–30 items per page.
- Cursors are nonempty ASCII strings of at most 30 characters. Ids are 0–1000000 and values are ASCII strings of length 0–50.
- Repeated ids may have different values. Repeated cursors and missing fixtures are valid test inputs.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Use three pages with a cap of `3`: `a` contains id `5` with value `first` and points to `b`; `b` is empty and points to `c`; `c` contains id `5` with value `later` plus id `8`, then ends. Requests must be `["a", "b", "c"]`. Keep id `5` with value `first`, then id `8`. The empty middle page contributes no items but still changes the next cursor and consumes one request.

### Read the existing code

Divide `solve` into five regions: guards, request recording, fixture lookup/status handling, item accumulation, and cursor progression. Track `seen_cursors` separately from `seen_ids`. Follow `requests`, `items`, and `error` through every `break`. Identify the rule that wins when a cursor is repeated exactly as the page cap is reached. There are no hidden transport helpers in this starter.

### Test before and after the change

Before Run, predict the full output for an empty middle page followed by one item. Then make that continuation missing, upstream-error, or cyclic in separate cases. Check requests as well as items and error. Test a terminal page exactly at the cap, a distinct next cursor beyond the cap, and a repeated cursor at the cap. Test duplicate IDs within and across pages with different values. Add an unreachable bad fixture to confirm it has no effect. These sequence tests check interactions that isolated one-page examples cannot show.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “Once the page cap has been reached, limit must be the reported error, even if the next cursor was already requested.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py`, my small diff, and my hand-derived page sequences. Trace each sequence through guards, request recording, fixture handling, deduplication, and continuation. Cite file lines. Identify a contract interaction my cases might miss. Do not implement the repair, refactor the client, or write tests. I will decide and verify any change.

### Technical completion checks

- Map the full data and control flow before changing continuation.
- Run hand-derived sequences that combine empty pages, duplicates, errors, and stop guards.
- Review the diff and the constructed AI claim independently. Judge success checks outputs; it does not assess your code navigation, test design, or production client safety.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 32 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Next, complete lab07 and lab08 from the guide.

Official documentation: [1](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api), [2](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
