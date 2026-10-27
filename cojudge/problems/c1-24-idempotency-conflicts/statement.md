# 24. Replay writes with idempotency keys

[Course list](/?course=capital-one-engineering-50) · Level 3 · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 20–23; state, validation, and response snapshots.

A client can lose a response after the server completes a write. Retrying the write without a stable identifier can create a second effect. An idempotency key names one logical request. The service stores the original body and result for that key. A retry with the same body gets the stored result. A different body must not silently reuse the key. The cache and the write need one atomic outcome in a real service. Here all operations are sequential and all bodies are valid. The exercise focuses on replay, conflicts, and identifier allocation. Cache expiration and concurrent requests are outside its scope.

</details>

**Scenario:** A mobile banking app sends each transfer request with an idempotency key. If the network fails, the app sends the same request again with the same key. The API must not create the transfer twice. A key that is reused for a different transfer is a client bug, so the API rejects it.

**Input:** `data` has:
- `requests`: a list of `{"key": string, "body": {"to": string, "amount": int}}`. All requests are valid.

**Rules:** process the requests in order. The key cache starts empty. Keys are case-sensitive.
- **New key:** create a transfer with the next id (1, 2, 3, …). Return `{"status": 201, "body": {"id": ..., "to": ..., "amount": ...}, "replayed": false}`.
- **Known key, same `to` and `amount`:** return its original body: `{"status": 201, "body": original body, "replayed": true}`.
- **Known key, different body:** return `{"status": 409, "body": {"error": "key_conflict"}, "replayed": false}`. A conflict changes nothing and does not use an id.

Compare the body fields, not the key order of the JSON.

**Return** `{"responses": [...], "transfers": [...]}`. `transfers` lists the created transfers in creation order.

This is a local policy in a simulated API, not an HTTP standard.

**Constraints:**

- 0–200 requests. Keys and recipients are nonempty ASCII strings of at most 40 characters.
- Amounts are integers from 1 through 1000000; booleans are excluded.
- Bodies contain exactly to and amount. Keys never expire during one call.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 29 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://docs.stripe.com/api/idempotent_requests)
