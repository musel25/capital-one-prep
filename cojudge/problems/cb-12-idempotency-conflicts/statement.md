# 12. Trace request identity through a replay cache

[Course list](/?course=capital-one-codebase-practice) · Level 3 · Medium · About 40 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 11. Trace a request through validation, lookup, and a state update.

The cache connects an idempotency key to the first body and result. The starter confuses a conflicting request with a replay. Your objective is to trace all state affected by new requests, replays, and conflicts, then repair the identity comparison.

A client can lose a response after the server completes a write. Retrying the write without a stable identifier can create a second effect. An idempotency key names one logical request. The service stores the original body and result for that key. A retry with the same body gets the stored result. A different body must not silently reuse the key. The cache and the write need one atomic outcome in a real service. Here all operations are sequential and all bodies are valid. The exercise focuses on replay, conflicts, and identifier allocation. Cache expiration and concurrent requests are outside its scope.

</details>

**Input:** `data` has:
- `requests`: a list of `{"key": string, "body": {"to": string, "amount": int}}`. All requests are valid.

**Rules:** process the requests in order. The key cache starts empty. Keys are case-sensitive.
- **New key:** create a transfer with the next id (1, 2, 3, …). Return `{"status": 201, "body": {"id": ..., "to": ..., "amount": ...}, "replayed": false}`.
- **Known key, same `to` and `amount`:** return its original body: `{"status": 201, "body": original body, "replayed": true}`.
- **Known key, different body:** return `{"status": 409, "body": {"error": "key_conflict"}, "replayed": false}`. A conflict changes nothing and does not use an id.

Compare the body fields, not the key order of the JSON.

**Return** `{"responses": [...], "transfers": [...]}`. `transfers` lists the created transfers in creation order.

This is a local policy in a simulated API, not an HTTP standard.

**What to fix:** The starter runs, but it has one intentional bug.

- Repair comparison of a request body with the saved body.
- Keep both recipient and amount significant.
- Preserve case-sensitive keys, original results, creation order, and consecutive IDs.
- A conflict must not replace the cache or consume an ID.
- Do not serialize dictionaries to compare their key order.
- Do not add expiry, retries, persistent storage, or concurrency.

**Constraints:**

- 0–200 requests. Keys and recipients are nonempty ASCII strings of at most 40 characters.
- Amounts are integers from 1 through 1000000; booleans are excluded.
- Bodies contain exactly to and amount. Keys never expire during one call.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Submit key `k` with recipient `Ada` and amount `4`: create transfer id `1`. Repeat that key and body: replay id `1`. Submit key `k` with recipient `Ada` and amount `5`: return 409. Submit key `m` with recipient `Bo` and amount `2`: create id `2`. There are four responses but only two transfers. Neither the replay nor the conflict allocates an ID.

### Read the existing code

Inspect `cache`, `transfers`, and `out` in `solve`. Trace the existing-key branch through `saved_body` and `result`. Then follow the new-key branch to ID allocation, cache insertion, and response construction. Identify which stored data establishes identity and which stored data supplies a replay response.

### Test before and after the change

Write the full expected responses for an original request, an amount-only change, and a replay of the original body. The final replay tests whether the conflict corrupted the cache. Test recipient-only changes, identical bodies with different keys, key case changes, and bodies with reversed field order. After a conflict, create a new key and check its ID. Assert transfers as well as response statuses; correct error output can hide an unwanted stored write.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “If the same body is sent under a new key, the service should replay the existing transfer.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py` and my expected request sequence. Trace which branches read and write `cache`, `transfers`, and `out`. Cite file lines. Check whether my cases distinguish replay from conflict and detect an ID gap. Do not supply the comparison, implementation, or test code.

### Technical completion checks

- Map cache, transfer, and response changes for all three request classes.
- Run conflict-then-replay and conflict-then-create sequences.
- Review ID allocation and saved-result preservation. Sequential judge checks do not prove safe concurrent idempotency.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 29 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Next, complete lab05 and lab06 from the guide.

Official documentation: [1](https://docs.stripe.com/api/idempotent_requests)
