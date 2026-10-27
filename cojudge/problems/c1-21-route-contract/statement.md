# 21. Route and method contracts

[Course list](/?course=capital-one-engineering-50) · Level 3 · Easy · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 1–20: dictionaries, functions, and state transitions.

An API contract defines the response for each route and method. A route selects a resource shape. A method selects an operation on that shape. Keep these decisions separate from the search for one stored record. A missing route and an unsupported method have different meanings. A successful delete can return no representation. Response bodies must also be snapshots: a later write must not change an earlier response. This exercise uses familiar HTTP status codes but defines a small explicit routing policy. It is a deterministic simulation. It does not start a server, parse a URL, or implement every HTTP rule.

</details>

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

**Constraints:**

- 0–100 items and 0–200 requests; ids and any numeric path suffix are at most 1000000.
- Names and paths have at most 80 ASCII characters. Methods are GET, DELETE, POST, PUT, PATCH, or HEAD.
- No network calls. Each solve call starts with its own items.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 30 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.rfc-editor.org/rfc/rfc9110.html)
