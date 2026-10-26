# 15. Track a shared time budget across calls

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 4 · Medium · About 40 minutes**

**Before this problem:** Exercise 14. Read retry decisions and integer time values.

## Learn first

Each step has its own timeout, but all steps spend one total budget. The starter mishandles arrival at an exact boundary. Your objective is to trace the remaining budget and distinguish a started operation from a completed operation.

A per-request timeout does not bound the total time of a sequence. Several individually acceptable waits can exceed a caller's deadline. Track one remaining budget across all operations. Before each request, limit its wait to the smaller of its own timeout and the remaining budget. Stop when either limit expires. Boundary rules must be explicit: this exercise accepts a response that arrives exactly at its allowance. It does not start another operation when no budget remains. The clock advances only by simulated waiting time. Real clients need a monotonic clock and must account for connection setup, processing, cancellation, and cleanup as well.

### Worked trace

Use budget `9` and two ok steps: duration `4`, timeout `8`; then duration `5`, timeout `7`. The allowances are `8` and `5`. Both responses arrive in time, so expect success with elapsed `9`, completed `2`, and started `2`. Append a zero-duration third step: it cannot start with no budget, so the result becomes deadline while the counters remain `9`, `2`, and `2`.

### Read the existing code

Inspect the `elapsed`, `completed`, and `started` counters in `solve`. Follow `remaining` into the start guard and `allowance`. Locate the arrival decision before the outcome check. Compare the timeout/deadline branch with the error branch. Explain why a timed-out step cannot reveal its supplied outcome to the caller.

## Your task

### Scoped repair

Repair the arrival boundary decision. Preserve equality as an observed response, shared-budget accounting, and the deadline priority when limits tie. Keep errors observed at the allowance distinct from responses that arrive too late. Do not reset the budget per step or add retries, sleep, CPU time, or a real clock.

### Required behavior

`budget` is a total time allowance in milliseconds. `steps` contains `{duration:int, timeout:int, outcome:"ok"|"error"}`. Start elapsed, completed, and started at zero. Before each step, if remaining budget is zero, stop with result deadline without starting it. Otherwise increment started and set allowance to min(timeout, remaining). If duration is greater than allowance, add allowance to elapsed and stop: result deadline when the shared budget binds, including a tie; otherwise timeout. If duration is at most allowance, add duration to elapsed. An error stops with result error; an ok increments completed. If all steps complete, result is success, even when the last response arrives exactly at the deadline. Return `{result, elapsed, completed, started}`. completed counts only ok steps. Empty steps always succeed.

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

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 16](/problems/cb-16-upstream-page-client).

## Examples

### Example 1: second step gets only remaining budget

Input to `solve`:
```json
{
  "budget": 10,
  "steps": [
    {
      "duration": 4,
      "timeout": 10,
      "outcome": "ok"
    },
    {
      "duration": 7,
      "timeout": 10,
      "outcome": "ok"
    }
  ]
}
```
Return:
```json
{
  "result": "deadline",
  "elapsed": 10,
  "completed": 1,
  "started": 2
}
```

### Example 2: per-step timeout can expire first

Input to `solve`:
```json
{
  "budget": 20,
  "steps": [
    {
      "duration": 8,
      "timeout": 5,
      "outcome": "ok"
    }
  ]
}
```
Return:
```json
{
  "result": "timeout",
  "elapsed": 5,
  "completed": 0,
  "started": 1
}
```

### Example 3: completion at deadline succeeds

Input to `solve`:
```json
{
  "budget": 10,
  "steps": [
    {
      "duration": 10,
      "timeout": 10,
      "outcome": "ok"
    }
  ]
}
```
Return:
```json
{
  "result": "success",
  "elapsed": 10,
  "completed": 1,
  "started": 1
}
```

## Constraints

- budget is 0–1000000. There are 0–200 steps.
- duration is 0–10000 and timeout is 1–10000. All clocks are integer milliseconds.
- No retries, CPU time, sleeps, or actual network calls.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 32 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://grpc.io/docs/guides/deadlines/)
- [Official documentation 2](https://docs.python.org/3/library/time.html#time.monotonic)
