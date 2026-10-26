# 09. Trace route, method, and record dispatch

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 3 · Easy · About 35 minutes**

**Before this problem:** Exercises 01–08 and local labs 01–04. The lesson introduces HTTP route decisions.

## Learn first

This is an API simulation inside `solve`, not a running web server. A request passes through route recognition, method checks, and record lookup. The starter returns the wrong result for a successful operation. Your objective is to locate the response branch while preserving dispatch order.

An API contract defines the response for each route and method. A route selects a resource shape. A method selects an operation on that shape. Keep these decisions separate from the search for one stored record. A missing route and an unsupported method have different meanings. A successful delete can return no representation. Response bodies must also be snapshots: a later write must not change an earlier response. This exercise uses familiar HTTP status codes but defines a small explicit routing policy. It is a deterministic simulation. It does not start a server, parse a URL, or implement every HTTP rule.

### Worked trace

Start with item `{"id": 4, "name": "pen"}`. Send `DELETE /items/4`, then `GET /items/4`, then `POST /items/4`. The responses must have statuses `204`, `404`, and `405`. The first body is null. The last response includes `allow: ["GET", "DELETE"]`, although the item is absent. The route still exists after its record is removed.

### Read the existing code

In `solve`, inspect `items`, `match`, and `allowed`. Follow the unknown-route branch, then the method branch, then the record lookup. Locate the delete mutation and its response construction. Inspect the copies used for collection and single-item bodies so a later request cannot change an earlier representation.

## Your task

### Scoped repair

Repair the successful deletion response. Preserve the actual deletion, missing-item response, exact path matching, method priority, and `allow` order. Keep `allow` absent from other responses. Do not normalize slashes, accept leading-zero IDs, add HEAD support, or change the simulation into a framework application.

### Required behavior

Implement `solve(data)`. `items` contains unique positive integer `id` values and string `name` values. `requests` contains `path` and uppercase `method` strings. Process requests in order. Return a list of response objects.

Exact routes: `GET /health` returns `{status:200, body:{status:"ok"}}`. `GET /items` returns status 200 and all item objects ordered by numeric id. `/items/N` matches only canonical positive decimal N. It allows GET then DELETE in that order. GET returns the item with status 200. DELETE removes it and returns `{status:204, body:null}`. Missing items return `{status:404, body:{error:"not_found"}}`. Unknown routes return the same 404. For a known route, check the method before record existence. Unsupported methods return `{status:405, body:{error:"method_not_allowed"}, allow:[...]}`. Collection and health allow only GET. Do not add an `allow` field to other responses. Paths are exact; no query or slash normalization.

### Test before and after the change

Before Run, write all response fields for the three-request trace. Test deleting twice, deleting a missing ID, and reading the collection before and after deletion. Test unsupported methods on both existing and missing records. Pair a known detail route with an unknown path to distinguish 405 from 404. Check `/items/04` and `/items/4/` as exact-path boundaries. Earlier collection output must still include the deleted item.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “An unsupported method on a canonical item route must return 405 before the program checks whether that item exists.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py`. Trace a DELETE on an existing item and a POST on a missing item. Cite file lines for route recognition, method validation, lookup, mutation, and response construction. Explain why the order matters under this contract. Do not write a router, patch, or response replacement.

### Technical completion checks

- Draw the route, method, and record decision order.
- Run a request sequence that verifies deletion and later reads.
- Review response fields and snapshots. Judge results cover this simulation, not a real HTTP server.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 10](/problems/cb-10-body-validation).

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
