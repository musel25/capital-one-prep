# 21. Route and method contracts

[Back to the course list](/?course=capital-one-engineering-50)

**Level 3 · Easy · About 25 minutes**

**Before this problem:** Problems 1–20: dictionaries, functions, and state transitions.

## Learn first

An API contract defines the response for each route and method. A route selects a resource shape. A method selects an operation on that shape. Keep these decisions separate from the search for one stored record. A missing route and an unsupported method have different meanings. A successful delete can return no representation. Response bodies must also be snapshots: a later write must not change an earlier response. This exercise uses familiar HTTP status codes but defines a small explicit routing policy. It is a deterministic simulation. It does not start a server, parse a URL, or implement every HTTP rule.

## Your task

Implement `solve(data)`. `items` contains unique positive integer `id` values and string `name` values. `requests` contains `path` and uppercase `method` strings. Process requests in order. Return a list of response objects.

Exact routes: `GET /health` returns `{status:200, body:{status:"ok"}}`. `GET /items` returns status 200 and all item objects ordered by numeric id. `/items/N` matches only canonical positive decimal N. It allows GET then DELETE in that order. GET returns the item with status 200. DELETE removes it and returns `{status:204, body:null}`. Missing items return `{status:404, body:{error:"not_found"}}`. Unknown routes return the same 404. For a known route, check the method before record existence. Unsupported methods return `{status:405, body:{error:"method_not_allowed"}, allow:[...]}`. Collection and health allow only GET. Do not add an `allow` field to other responses. Paths are exact; no query or slash normalization.

## Examples

### Example 1: collection is ordered by numeric id

Input to `solve`:
```json
{
  "items": [
    {
      "id": 2,
      "name": "book"
    },
    {
      "id": 1,
      "name": "pen"
    }
  ],
  "requests": [
    {
      "path": "/items",
      "method": "GET"
    }
  ]
}
```
Return:
```json
[
  {
    "status": 200,
    "body": [
      {
        "id": 1,
        "name": "pen"
      },
      {
        "id": 2,
        "name": "book"
      }
    ]
  }
]
```

### Example 2: delete then read

Input to `solve`:
```json
{
  "items": [
    {
      "id": 1,
      "name": "pen"
    }
  ],
  "requests": [
    {
      "path": "/items/1",
      "method": "DELETE"
    },
    {
      "path": "/items/1",
      "method": "GET"
    }
  ]
}
```
Return:
```json
[
  {
    "status": 204,
    "body": null
  },
  {
    "status": 404,
    "body": {
      "error": "not_found"
    }
  }
]
```

### Example 3: method check precedes item lookup

Input to `solve`:
```json
{
  "items": [],
  "requests": [
    {
      "path": "/items/9",
      "method": "POST"
    }
  ]
}
```
Return:
```json
[
  {
    "status": 405,
    "body": {
      "error": "method_not_allowed"
    },
    "allow": [
      "GET",
      "DELETE"
    ]
  }
]
```

## Constraints

- 0–100 items and 0–200 requests; ids and any numeric path suffix are at most 1000000.
- Names and paths have at most 80 ASCII characters. Methods are GET, DELETE, POST, PUT, PATCH, or HEAD.
- No network calls. Each solve call starts with its own items.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 30 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://www.rfc-editor.org/rfc/rfc9110.html)
