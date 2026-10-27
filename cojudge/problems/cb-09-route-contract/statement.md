# 09. Trace route, method, and record dispatch

[Course list](/?course=capital-one-codebase-practice) · Level 3 · Easy · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercises 01–08 and local labs 01–04. The lesson introduces HTTP route decisions.

This is an API simulation inside `solve`, not a running web server. A request passes through route recognition, method checks, and record lookup. The starter returns the wrong result for a successful operation. Your objective is to locate the response branch while preserving dispatch order.

An API contract defines the response for each route and method. A route selects a resource shape. A method selects an operation on that shape. Keep these decisions separate from the search for one stored record. A missing route and an unsupported method have different meanings. A successful delete can return no representation. Response bodies must also be snapshots: a later write must not change an earlier response. This exercise uses familiar HTTP status codes but defines a small explicit routing policy. It is a deterministic simulation. It does not start a server, parse a URL, or implement every HTTP rule.

</details>

**Scenario:** You build a small HTTP API for an internal inventory tool. There is no real server: `solve` gets the stored items and a list of requests, and returns the response to each request, in order.

> **Bug report:** "When I delete an item, the API answers 404 Not Found, so the app shows an error. But the item is gone, so the delete worked."

**Input:** `data` has:
- `items`: a list of `{"id": int, "name": string}`. IDs are unique positive integers.
- `requests`: a list of `{"path": string, "method": string}`. Methods are uppercase.

Process the requests in order. **Return** a list with one response object per request.

**Routes:** paths must match exactly. There is no query parsing and no slash normalization.

| Route | Allowed methods |
| --- | --- |
| `/health` | GET |
| `/items` | GET |
| `/items/N` | GET, DELETE |

`N` matches only a canonical positive decimal number. For example, `/items/01`, `/items/0`, `/items/+1`, and `/items/1/` are unknown routes.

**Responses**
- `GET /health` → `{"status": 200, "body": {"status": "ok"}}`
- `GET /items` → `{"status": 200, "body": [all items, sorted by id]}`
- `GET /items/N` → `{"status": 200, "body": item}`
- `DELETE /items/N` → remove the item and return `{"status": 204, "body": null}`
- Item `N` does not exist → `{"status": 404, "body": {"error": "not_found"}}`
- Unknown route → the same 404 response.
- Known route, method not allowed → `{"status": 405, "body": {"error": "method_not_allowed"}, "allow": [...]}`. `allow` lists the allowed methods in the table order, for example `["GET", "DELETE"]`.

On a known route, check the method before you check that the item exists. Only 405 responses have an `allow` field.

**What to fix:** The starter runs, but it has one intentional bug.

- Repair the successful deletion response.
- Preserve the actual deletion, missing-item response, exact path matching, method priority, and `allow` order.
- Keep `allow` absent from other responses.
- Do not normalize slashes, accept leading-zero IDs, add HEAD support, or change the simulation into a framework application.

**Constraints:**

- 0–100 items and 0–200 requests; ids and any numeric path suffix are at most 1000000.
- Names and paths have at most 80 ASCII characters. Methods are GET, DELETE, POST, PUT, PATCH, or HEAD.
- No network calls. Each solve call starts with its own items.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Start with item `{"id": 4, "name": "pen"}`. Send `DELETE /items/4`, then `GET /items/4`, then `POST /items/4`. The responses must have statuses `204`, `404`, and `405`. The first body is null. The last response includes `allow: ["GET", "DELETE"]`, although the item is absent. The route still exists after its record is removed.

### Read the existing code

In `solve`, inspect `items`, `match`, and `allowed`. Follow the unknown-route branch, then the method branch, then the record lookup. Locate the delete mutation and its response construction. Inspect the copies used for collection and single-item bodies so a later request cannot change an earlier representation.

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

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 30 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 10](/problems/cb-10-body-validation).

Official documentation: [1](https://www.rfc-editor.org/rfc/rfc9110.html)
