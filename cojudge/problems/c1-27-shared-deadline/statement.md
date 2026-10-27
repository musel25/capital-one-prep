# 27. Spend one timeout budget

[Course list](/?course=capital-one-engineering-50) · Level 3 · Medium · About 30 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Problem 26; integer clocks and sequential client operations.

A per-request timeout does not bound the total time of a sequence. Several individually acceptable waits can exceed a caller's deadline. Track one remaining budget across all operations. Before each request, limit its wait to the smaller of its own timeout and the remaining budget. Stop when either limit expires. Boundary rules must be explicit: this exercise accepts a response that arrives exactly at its allowance. It does not start another operation when no budget remains. The clock advances only by simulated waiting time. Real clients need a monotonic clock and must account for connection setup, processing, cancellation, and cleanup as well.

</details>

**Scenario:** A checkout request must finish within a total time budget. It calls several services in order, and each call has its own timeout. `solve` simulates how much time the request uses and why it stops.

**Input:** `data` has:
- `budget`: the total time allowance, in milliseconds.
- `steps`: a list of `{"duration": int, "timeout": int, "outcome": "ok" | "error"}`.

**Rules:** `elapsed`, `completed`, and `started` start at 0. For each step, in order:
1. If the remaining budget (`budget - elapsed`) is 0, stop with `deadline`. Do not start the step.
2. Add 1 to `started`. Set `allowance = min(timeout, remaining budget)`.
3. If `duration > allowance`: add `allowance` to `elapsed` and stop. The result is `deadline` if the shared budget was the limit (allowance = remaining budget, also when `timeout` is equal to it). Otherwise the result is `timeout`.
4. Otherwise add `duration` to `elapsed`. If the outcome is `error`, stop with `error`. If it is `ok`, add 1 to `completed`.

If all steps finish, the result is `success`, even when the last step ends exactly at the deadline. An empty `steps` list gives `success`.

**Return** `{"result": string, "elapsed": int, "completed": int, "started": int}`. `completed` counts only `ok` steps.

**Constraints:**

- budget is 0–1000000. There are 0–200 steps.
- duration is 0–10000 and timeout is 1–10000. All clocks are integer milliseconds.
- No retries, CPU time, sleeps, or actual network calls.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 32 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://grpc.io/docs/guides/deadlines/), [2](https://docs.python.org/3/library/time.html#time.monotonic)
