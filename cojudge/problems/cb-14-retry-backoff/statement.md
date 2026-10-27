# 14. Separate failure classification from retry scheduling

[Course list](/?course=capital-one-codebase-practice) · Level 4 · Medium · About 35 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 13. Follow an ordered list of outcomes and a retry counter.

The retry loop classifies one outcome before it decides whether another attempt can run. The starter retries a class of failure that must stop. Your objective is to locate that policy decision while preserving attempt counts and delay placement.

A retry policy needs three decisions: which failures are temporary, how many attempts are allowed, and how long to wait between attempts. Retrying every failure can repeat a permanent error and overload a service. Exponential backoff increases delays after repeated temporary failures. A cap bounds each delay. An attempt limit includes the first request, so three attempts allow at most two waits. Production clients often add random jitter and honor server guidance. This exercise excludes both to make results deterministic. Its retry set is an explicit local policy. Apply it to an operation that is safe to repeat, such as a read or a protected write.

</details>

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

**What to fix:** The starter runs, but it has one intentional bug.

- Repair only the retryable-outcome classification.
- Preserve the exact allowlist, 200–299 success range, attempt limit, exponential delay sequence, and cap.
- Keep `failed` distinct from `exhausted`.
- Do not add jitter, Retry-After handling, sleeping, real transport, or an overall deadline.
- This task supplies an explicit policy rather than a universal HTTP rule.

**Constraints:**

- max_attempts is 1–10. outcomes contains at least max_attempts and at most 30 entries.
- Statuses are integers 100–599. base is 1–1000 and cap is 1–10000, in milliseconds.
- The exercise has no Retry-After header, jitter, or overall deadline.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Use outcomes `[503, "timeout", 204, 500]`, `max_attempts = 4`, `base = 3`, and `cap = 5`. Attempt 1 records delay `3`. Attempt 2 records delay `5`. Attempt 3 succeeds. Expect `{"attempts": 3, "delays": [3, 5], "result": "success"}`. The final 500 is unused. A delay belongs between attempts, not after the last outcome that the program consumes.

### Read the existing code

In `solve`, inspect `index`, `attempts`, `retryable`, and `delays`. Follow the return paths in order: success, non-retryable failure, and exhausted attempts. Then inspect delay construction. Mark which branch determines the error class and which branch determines whether capacity remains for another call.

### Test before and after the change

Predict outcomes `[501, 200]` with two allowed attempts before Run. Compare them with `[502, 200]`. Test every listed retryable class, a terminal response after a retry, 199/200 and 299/300 boundaries, and a single allowed retryable attempt. Check a cap below the base and a cap reached after several retries. Assert exact delays and attempts, not only the final result. Unused outcomes must not affect any output.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “Status 501 stops with failed under this policy, even when more attempts and a later success outcome are available.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py`, the retry policy, and my case table. Cite file lines that classify outcomes, stop at the attempt limit, and append delays. Review whether each expected result follows the stated policy. Do not write a replacement condition, retry loop, or tests.

### Technical completion checks

- Write the classification table separately from the delay sequence.
- Run terminal, retryable, success-boundary, and final-attempt cases.
- Review stop order and unused outcomes. The deterministic judge does not measure actual network retry behavior.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 32 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 15](/problems/cb-15-shared-deadline).

Official documentation: [1](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
