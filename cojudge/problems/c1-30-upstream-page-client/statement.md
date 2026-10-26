# 30. Build a guarded upstream page client

[Back to the course list](/?course=capital-one-engineering-50)

**Level 3 · Hard · About 40 minutes**

**Before this problem:** Problems 21–29; sets, pagination, and bounded client policies.

## Learn first

A pagination client needs a completion condition and guards against faulty upstream behavior. An empty page can still point to another page. Repeated records need a documented merge rule. A repeated cursor can create an infinite loop unless the client remembers which cursors it already requested. A separate page cap also stops a long chain of distinct cursors. Decide what happens to useful data when a later page fails. This exercise keeps the accepted prefix and reports the failure. The pages are supplied fixtures, so the client makes no network calls. Combining these rules checks control flow that a single happy-path page cannot reveal.

## Your task

Input has `start` cursor, `max_pages`, and `pages`, an object mapping cursors to page fixtures. Successful pages are `{status:200, items:[{id:int,value:string},...], next:string|null}`. Error pages contain only status, either 429 or 500–599. Begin at start. Before each fetch: first stop with error cycle if this cursor was already requested; otherwise stop with limit if max_pages were requested. Append the cursor to requests. A missing fixture stops with missing. An error page stops with upstream. Successful pages append only the first occurrence of each item id, preserving traversal order and its first value. Follow next even after an empty items list. Null next ends successfully. Return `{items:[...], requests:[cursor,...], error:null|"cycle"|"limit"|"missing"|"upstream"}`. Keep earlier items on failure. Do not retry. Unreachable fixtures are ignored.

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
