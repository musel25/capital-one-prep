# 16. Review the full path through a paged client

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 4 · Hard · About 50 minutes**

**Before this problem:** Exercises 13–15. Trace cursor, duplicate, timeout, and error state through one loop.

## Learn first

This final browser task combines traversal, duplicate handling, stop guards, and partial results in one `solve` function. The starter stops before following a valid continuation. Your objective is to repair cursor progression and then review its interactions with every existing guard. The pages are fixtures; no network is used.

A pagination client needs a completion condition and guards against faulty upstream behavior. An empty page can still point to another page. Repeated records need a documented merge rule. A repeated cursor can create an infinite loop unless the client remembers which cursors it already requested. A separate page cap also stops a long chain of distinct cursors. Decide what happens to useful data when a later page fails. This exercise keeps the accepted prefix and reports the failure. The pages are supplied fixtures, so the client makes no network calls. Combining these rules checks control flow that a single happy-path page cannot reveal.

### Worked trace

Use three pages with a cap of `3`: `a` contains id `5` with value `first` and points to `b`; `b` is empty and points to `c`; `c` contains id `5` with value `later` plus id `8`, then ends. Requests must be `["a", "b", "c"]`. Keep id `5` with value `first`, then id `8`. The empty middle page contributes no items but still changes the next cursor and consumes one request.

### Read the existing code

Divide `solve` into five regions: guards, request recording, fixture lookup/status handling, item accumulation, and cursor progression. Track `seen_cursors` separately from `seen_ids`. Follow `requests`, `items`, and `error` through every `break`. Identify the rule that wins when a cursor is repeated exactly as the page cap is reached. There are no hidden transport helpers in this starter.

## Your task

### Scoped repair

Repair continuation after a successful page. Preserve cycle-before-limit priority, attempted-request recording, first-value-wins deduplication, and accepted items on failure. Keep null next as completion. Do not treat an empty item list as an error. Do not add retries or change the meaning of the cap. Keep unreachable fixtures irrelevant.

### Required behavior

Input has `start` cursor, `max_pages`, and `pages`, an object mapping cursors to page fixtures. Successful pages are `{status:200, items:[{id:int,value:string},...], next:string|null}`. Error pages contain only status, either 429 or 500–599. Begin at start. Before each fetch: first stop with error cycle if this cursor was already requested; otherwise stop with limit if max_pages were requested. Append the cursor to requests. A missing fixture stops with missing. An error page stops with upstream. Successful pages append only the first occurrence of each item id, preserving traversal order and its first value. Follow next even after an empty items list. Null next ends successfully. Return `{items:[...], requests:[cursor,...], error:null|"cycle"|"limit"|"missing"|"upstream"}`. Keep earlier items on failure. Do not retry. Unreachable fixtures are ignored.

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

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Next, complete lab07 and lab08 from the guide.

## Examples

### Example 1: deduplicate across pages

Input to `solve`:
```json
{
  "pages": {
    "a": {
      "status": 200,
      "items": [
        {
          "id": 1,
          "value": "1"
        }
      ],
      "next": "b"
    },
    "b": {
      "status": 200,
      "items": [
        {
          "id": 1,
          "value": "1"
        },
        {
          "id": 2,
          "value": "2"
        }
      ],
      "next": null
    }
  },
  "start": "a",
  "max_pages": 5
}
```
Return:
```json
{
  "items": [
    {
      "id": 1,
      "value": "1"
    },
    {
      "id": 2,
      "value": "2"
    }
  ],
  "requests": [
    "a",
    "b"
  ],
  "error": null
}
```

### Example 2: stop before fetching a repeated cursor

Input to `solve`:
```json
{
  "pages": {
    "a": {
      "status": 200,
      "items": [
        {
          "id": 1,
          "value": "1"
        }
      ],
      "next": "a"
    }
  },
  "start": "a",
  "max_pages": 5
}
```
Return:
```json
{
  "items": [
    {
      "id": 1,
      "value": "1"
    }
  ],
  "requests": [
    "a"
  ],
  "error": "cycle"
}
```

### Example 3: preserve earlier data on failure

Input to `solve`:
```json
{
  "pages": {
    "a": {
      "status": 200,
      "items": [
        {
          "id": 1,
          "value": "1"
        }
      ],
      "next": "b"
    },
    "b": {
      "status": 503
    }
  },
  "start": "a",
  "max_pages": 5
}
```
Return:
```json
{
  "items": [
    {
      "id": 1,
      "value": "1"
    }
  ],
  "requests": [
    "a",
    "b"
  ],
  "error": "upstream"
}
```

## Constraints

- 1–20 max_pages; 0–30 page fixtures; 0–30 items per page.
- Cursors are nonempty ASCII strings of at most 30 characters. Ids are 0–1000000 and values are ASCII strings of length 0–50.
- Repeated ids may have different values. Repeated cursors and missing fixtures are valid test inputs.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 32 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api)
- [Official documentation 2](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset)
