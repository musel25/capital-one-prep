# 30. Build a guarded upstream page client

[Course list](/?course=capital-one-engineering-50) · Level 3 · Hard · About 40 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 21–29; sets, pagination, and bounded client policies.

A pagination client needs a completion condition and guards against faulty upstream behavior. An empty page can still point to another page. Repeated records need a documented merge rule. A repeated cursor can create an infinite loop unless the client remembers which cursors it already requested. A separate page cap also stops a long chain of distinct cursors. Decide what happens to useful data when a later page fails. This exercise keeps the accepted prefix and reports the failure. The pages are supplied fixtures, so the client makes no network calls. Combining these rules checks control flow that a single happy-path page cannot reveal.

</details>

**Scenario:** Your service downloads a full list from a partner API, page by page, and follows the `next` cursor of each page. The partner API is unreliable: it can loop, fail, or point to pages that do not exist. Your client must stop safely and keep what it already has. `pages` is a recorded copy of the partner's responses.

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

**Constraints:**

- 1–20 max_pages; 0–30 page fixtures; 0–30 items per page.
- Cursors are nonempty ASCII strings of at most 30 characters. Ids are 0–1000000 and values are ASCII strings of length 0–50.
- Repeated ids may have different values. Repeated cursors and missing fixtures are valid test inputs.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 32 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api), [2](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
