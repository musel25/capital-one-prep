# 45. Trace a circuit breaker through recovery

[Back to the course list](/?course=capital-one-engineering-50)

**Level 5 · Hard · About 35 minutes**

**Before this problem:** State machines, consecutive counters, and time boundaries.

## Learn first

A circuit breaker stops repeated calls to a failing dependency. While closed, it allows calls and counts consecutive failures. Enough failures open the breaker for a cooldown period. During that period calls are blocked and do not reach the dependency. At the deadline, the next call is a half-open probe. A successful probe closes the breaker and resets failures. A failed probe opens it for a new cooldown. The half-open state is transient here because each allowed call completes immediately in the trace. This exercise uses supplied outcomes and integer times. It is a deterministic event trace, not an actual parallel, thread, or network test.

## Your task

Input has positive `threshold`, positive `cooldown`, and `calls` with nondecreasing `at` times and Boolean `ok` outcomes. Start closed with zero failures. A closed success resets failures; a closed failure increments them and opens the breaker when the threshold is reached. Opening sets `retry_at = at + cooldown`. While open and `at < retry_at`, block calls and ignore their outcome. At or after the deadline allow one half-open probe. Probe success closes and resets; probe failure increments failures and opens for a new cooldown regardless of threshold. Return `{results, state, failures, retry_at}`. Each result is `{mode, result, state}`: mode is `closed`, `probe`, or `blocked`; result is `success`, `failure`, or `blocked`; state is the state after that call. Final retry_at is null when closed. Blocked calls change nothing.

## Examples

### Example 1: consecutive failures open breaker

Input to `solve`:
```json
{
  "threshold": 2,
  "cooldown": 5,
  "calls": [
    {
      "at": 0,
      "ok": false
    },
    {
      "at": 1,
      "ok": false
    }
  ]
}
```
Return:
```json
{
  "results": [
    {
      "mode": "closed",
      "result": "failure",
      "state": "closed"
    },
    {
      "mode": "closed",
      "result": "failure",
      "state": "open"
    }
  ],
  "state": "open",
  "failures": 2,
  "retry_at": 6
}
```

### Example 2: open breaker ignores supplied outcome

Input to `solve`:
```json
{
  "threshold": 1,
  "cooldown": 5,
  "calls": [
    {
      "at": 0,
      "ok": false
    },
    {
      "at": 4,
      "ok": true
    }
  ]
}
```
Return:
```json
{
  "results": [
    {
      "mode": "closed",
      "result": "failure",
      "state": "open"
    },
    {
      "mode": "blocked",
      "result": "blocked",
      "state": "open"
    }
  ],
  "state": "open",
  "failures": 1,
  "retry_at": 5
}
```

### Example 3: probe succeeds at deadline

Input to `solve`:
```json
{
  "threshold": 1,
  "cooldown": 5,
  "calls": [
    {
      "at": 0,
      "ok": false
    },
    {
      "at": 5,
      "ok": true
    }
  ]
}
```
Return:
```json
{
  "results": [
    {
      "mode": "closed",
      "result": "failure",
      "state": "open"
    },
    {
      "mode": "probe",
      "result": "success",
      "state": "closed"
    }
  ],
  "state": "closed",
  "failures": 0,
  "retry_at": null
}
```

## Constraints

- 0–300 calls; threshold is 1–100, cooldown is 1–1000000, at is 0–1000000.
- No call remains in flight between trace entries.

## Work here

Select **Python**. Edit `solve(data)` and its helper code. The supplied
`Solution.run` adapter converts the judge's JSON text into normal Python values.
You do not need to edit the adapter or escape JSON by hand. For a custom test,
paste a JSON object into the `payload` field.

Use **Run** for the three examples. Use **Submit** for all 36 tests.
Open one hint if you need help. The reference solution is optional.

The judge checks output behavior. It does not certify type annotations,
inheritance, SQL use, or time complexity. Follow the requested technique to
practice the skill. A code review can check those implementation choices.

This is an original constructed exercise. It is not an official Capital One
question. All data is fictional. Completing this course does not certify
interview readiness.

## References

- [Official documentation 1](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
