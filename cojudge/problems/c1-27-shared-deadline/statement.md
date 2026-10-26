# 27. Spend one timeout budget

[Back to the course list](/?course=capital-one-engineering-50)

**Level 3 · Medium · About 30 minutes**

**Before this problem:** Problem 26; integer clocks and sequential client operations.

## Learn first

A per-request timeout does not bound the total time of a sequence. Several individually acceptable waits can exceed a caller's deadline. Track one remaining budget across all operations. Before each request, limit its wait to the smaller of its own timeout and the remaining budget. Stop when either limit expires. Boundary rules must be explicit: this exercise accepts a response that arrives exactly at its allowance. It does not start another operation when no budget remains. The clock advances only by simulated waiting time. Real clients need a monotonic clock and must account for connection setup, processing, cancellation, and cleanup as well.

## Your task

`budget` is a total time allowance in milliseconds. `steps` contains `{duration:int, timeout:int, outcome:"ok"|"error"}`. Start elapsed, completed, and started at zero. Before each step, if remaining budget is zero, stop with result deadline without starting it. Otherwise increment started and set allowance to min(timeout, remaining). If duration is greater than allowance, add allowance to elapsed and stop: result deadline when the shared budget binds, including a tie; otherwise timeout. If duration is at most allowance, add duration to elapsed. An error stops with result error; an ok increments completed. If all steps complete, result is success, even when the last response arrives exactly at the deadline. Return `{result, elapsed, completed, started}`. completed counts only ok steps. Empty steps always succeed.

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
