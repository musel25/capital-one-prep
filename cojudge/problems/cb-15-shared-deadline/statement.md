# 15. Track a shared time budget across calls

[Course list](/?course=capital-one-codebase-practice) · Level 4 · Medium · About 40 minutes

<details>
<summary><strong>Lesson</strong> (open it first if the topic is new)</summary>

**Before this problem:** Exercise 14. Read retry decisions and integer time values.

Each step has its own timeout, but all steps spend one total budget. The starter mishandles arrival at an exact boundary. Your objective is to trace the remaining budget and distinguish a started operation from a completed operation.

A per-request timeout does not bound the total time of a sequence. Several individually acceptable waits can exceed a caller's deadline. Track one remaining budget across all operations. Before each request, limit its wait to the smaller of its own timeout and the remaining budget. Stop when either limit expires. Boundary rules must be explicit: this exercise accepts a response that arrives exactly at its allowance. It does not start another operation when no budget remains. The clock advances only by simulated waiting time. Real clients need a monotonic clock and must account for connection setup, processing, cancellation, and cleanup as well.

</details>

**Scenario:** A checkout request must finish within a total time budget. It calls several services in order, and each call has its own timeout. `solve` simulates how much time the request uses and why it stops.

> **Bug report:** "A service answered in exactly 5 ms, and its timeout is 5 ms. The request was marked as a timeout, but the answer arrived in time."

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

**What to fix:** The starter runs, but it has one intentional bug.

- Repair the arrival boundary decision.
- Preserve equality as an observed response, shared-budget accounting, and the deadline priority when limits tie.
- Keep errors observed at the allowance distinct from responses that arrive too late.
- Do not reset the budget per step or add retries, sleep, CPU time, or a real clock.

**Constraints:**

- budget is 0–1000000. There are 0–200 steps.
- duration is 0–10000 and timeout is 1–10000. All clocks are integer milliseconds.
- No retries, CPU time, sleeps, or actual network calls.

<details>
<summary><strong>Practice steps</strong> (trace, tests, AI review)</summary>

### Worked trace

Use budget `9` and two ok steps: duration `4`, timeout `8`; then duration `5`, timeout `7`. The allowances are `8` and `5`. Both responses arrive in time, so expect success with elapsed `9`, completed `2`, and started `2`. Append a zero-duration third step: it cannot start with no budget, so the result becomes deadline while the counters remain `9`, `2`, and `2`.

### Read the existing code

Inspect the `elapsed`, `completed`, and `started` counters in `solve`. Follow `remaining` into the start guard and `allowance`. Locate the arrival decision before the outcome check. Compare the timeout/deadline branch with the error branch. Explain why a timed-out step cannot reveal its supplied outcome to the caller.

### Test before and after the change

Predict duration one below, equal to, and one above an allowance. Exercise a per-step timeout that is smaller than remaining budget, then a shared budget that is smaller, then a tie. Pair exact-boundary ok and error outcomes. Test zero budget with no steps and with a zero-duration step. Test an exact final completion and an attempted later step. Assert all four output fields: a correct result label can still hide a started or completed counter error.

### Check an AI claim

The following claim is a constructed review example. It may be correct or incorrect. Check it against the code and contract.

> Constructed AI claim to audit: “A zero-duration step can always start, even when the shared budget is already zero.”

Optional AI prompt. Write your own implementation and tests:

> I will paste `solution.py` and my time table. Cite file lines for the start guard, allowance, arrival decision, elapsed update, and outcome handling. Check my predicted counters for exact-boundary cases. Do not write a comparison, implementation, or tests. I will make the repair and verify it.

### Technical completion checks

- Write a time table with remaining budget, allowance, and all counters.
- Run below/equal/above boundary cases for both time limits.
- Review response and start ordering. Simulated integer time does not prove real deadline enforcement.

A judge pass checks behavior. Your trace, test choice, and edit scope need your review. Do not use the pass mark as evidence of those skills.

</details>

---

Select **Python** and edit `solve(data)`. Do not edit the `Solution.run` adapter: it converts the
judge's JSON for you. For a custom test, paste a JSON object into `payload`. **Run** checks the
three examples. **Submit** runs all 32 tests.

The judge checks only the output. It does not check type annotations, inheritance, SQL use, or
time complexity. This is an original practice exercise, not an official Capital One question. All
data is fictional. Completing it does not prove interview readiness.

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 16](/problems/cb-16-upstream-page-client).

Official documentation: [1](https://grpc.io/docs/guides/deadlines/), [2](https://docs.python.org/3/library/time.html#time.monotonic)
