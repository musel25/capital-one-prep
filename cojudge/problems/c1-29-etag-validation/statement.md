# 29. Validate cached representations with ETags

[Course list](/?course=capital-one-engineering-50) · Level 3 · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 21–24; request contracts and versioned state.

A cached response can carry a validator called an entity tag, or ETag. The client later sends that tag with a conditional read. If it still matches, the server can return a not-modified response without the representation body. The client then keeps its cached body. For If-None-Match on GET, weak tags can match the same underlying tag value. A write can change the current validator. This exercise uses an integer version to create simple tags and supplies an already parsed list of client tags. It covers validation, not cache freshness, expiration, header parsing, or a complete HTTP cache implementation.

</details>

**Input:** `data` has:
- `initial`: `{"version": positive int, "body": string}`.
- `requests`: a list of `{"op": "put", "body": string}` or `{"op": "get", "tags": null | [tag, ...]}`.

**ETag:** the current ETag is the string `"vN"`, including the two quote characters, where N is the current version.

**Rules**
- `put`: add 1 to the version (also if the body did not change) and store the body. Return `{"status": 200, "etag": current tag, "body": current body}`.
- `get` with `"tags": null`: there is no validator. Return status 200 with the etag and the body.
- `get` with a tags list: a tag matches if it is `*`, the current tag, or `W/` followed by the current tag.
  - Any tag matches → `{"status": 304, "etag": current tag, "body": null}`.
  - No match → status 200 with the etag and the body.

The resource always exists. The tags are already parsed.

**Return** the responses in request order.

**Constraints:**

- 0–200 requests; initial version is 1–1000000. Bodies are ASCII strings of length 0–200.
- A tags list has 0–20 entries. Each is *, a quoted vN tag, or W/ followed by a quoted vN tag; N is 1–1000000.
- Tags are pre-parsed; malformed tags and cache expiration are outside the domain.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 29 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://www.rfc-editor.org/rfc/rfc9110.html#name-if-none-match), [2](https://www.rfc-editor.org/rfc/rfc9111.html)
