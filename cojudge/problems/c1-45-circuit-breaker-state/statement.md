# 45. Trace a circuit breaker through recovery

[Course list](/?course=capital-one-engineering-50) · Level 5 · Hard · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** State machines, consecutive counters, and time boundaries.

A circuit breaker stops repeated calls to a failing dependency. While closed, it allows calls and counts consecutive failures. Enough failures open the breaker for a cooldown period. During that period calls are blocked and do not reach the dependency. At the deadline, the next call is a half-open probe. A successful probe closes the breaker and resets failures. A failed probe opens it for a new cooldown. The half-open state is transient here because each allowed call completes immediately in the trace. This exercise uses supplied outcomes and integer times. It is a deterministic event trace, not an actual parallel, thread, or network test.

</details>

**Input:** `data` has:
- `threshold`, `cooldown`: positive integers.
- `calls`: a list of `{"at": int, "ok": bool}`. Times never decrease.

**Rules:** the breaker starts `closed` with 0 failures. Opening the breaker sets `retry_at = at + cooldown`.
- **Closed:** a success resets failures to 0. A failure adds 1 to failures, and the breaker opens when failures reach `threshold`.
- **Open and `at < retry_at`:** block the call and ignore its outcome. A blocked call changes nothing.
- **Open and `at` ≥ `retry_at`:** allow one half-open probe. A success closes the breaker and resets failures to 0. A failure adds 1 to failures and opens the breaker for a new cooldown, whatever the threshold.

**Return** `{"results": [...], "state": ..., "failures": ..., "retry_at": ...}`
- `results`: one `{"mode": ..., "result": ..., "state": ...}` per call. `mode` is `closed`, `probe`, or `blocked`. `result` is `success`, `failure`, or `blocked`. `state` is the state after the call.
- `retry_at` is `null` when the final state is closed.

**Constraints:**

- 0–300 calls; threshold is 1–100, cooldown is 1–1000000, at is 0–1000000.
- No call remains in flight between trace entries.

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 36 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

Official documentation: [1](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
