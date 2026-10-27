# 26. Classify retries and cap backoff

[Course list](/?course=capital-one-engineering-50) · Level 3 · Medium · About 25 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problems 21–25; loops, status codes, and bounded state.

A retry policy needs three decisions: which failures are temporary, how many attempts are allowed, and how long to wait between attempts. Retrying every failure can repeat a permanent error and overload a service. Exponential backoff increases delays after repeated temporary failures. A cap bounds each delay. An attempt limit includes the first request, so three attempts allow at most two waits. Production clients often add random jitter and honor server guidance. This exercise excludes both to make results deterministic. Its retry set is an explicit local policy. Apply it to an operation that is safe to repeat, such as a read or a protected write.

</details>

**Scenario:** A payment client calls a bank API. Some failures are temporary (timeouts, 429, and some 5xx errors), and the client retries them with exponential backoff. Other failures, such as 400, are permanent, and the client must stop at once. `outcomes` lists what the API returns on each attempt.

**Input:** `data` has:
- `outcomes`: a list. Each entry is an integer HTTP status or the string `"timeout"`.
- `max_attempts`: the maximum number of attempts.
- `base`, `cap`: integers, in milliseconds.

**Rules:** use one outcome per attempt, in order, for at most `max_attempts` attempts.
- Status 200–299 → stop with `success`.
- Retryable outcomes are only `"timeout"` and the statuses 429, 500, 502, 503, and 504.
- Any other status → stop with `failed`.
- A retryable outcome on the last allowed attempt → stop with `exhausted`.
- A retryable outcome with attempts left → record a delay, then retry. Before retry number k (k starts at 1), the delay is `min(cap, base * 2**(k-1))`.

Record a delay only when another attempt will run. Ignore unused outcomes. Do not sleep or make network calls.

**Return** `{"attempts": int, "delays": [int], "result": "success" | "failed" | "exhausted"}`.

**Constraints:**

- max_attempts is 1–10. outcomes contains at least max_attempts and at most 30 entries.
- Statuses are integers 100–599. base is 1–1000 and cap is 1–10000, in milliseconds.
- The exercise has no Retry-After header, jitter, or overall deadline.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 32 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
