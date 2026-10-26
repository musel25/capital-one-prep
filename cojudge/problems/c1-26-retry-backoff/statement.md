# 26. Classify retries and cap backoff

[Back to the course list](/?course=capital-one-engineering-50)

**Level 3 · Medium · About 25 minutes**

**Before this problem:** Problems 21–25; loops, status codes, and bounded state.

## Learn first

A retry policy needs three decisions: which failures are temporary, how many attempts are allowed, and how long to wait between attempts. Retrying every failure can repeat a permanent error and overload a service. Exponential backoff increases delays after repeated temporary failures. A cap bounds each delay. An attempt limit includes the first request, so three attempts allow at most two waits. Production clients often add random jitter and honor server guidance. This exercise excludes both to make results deterministic. Its retry set is an explicit local policy. Apply it to an operation that is safe to repeat, such as a read or a protected write.

## Your task

Input fields are `outcomes`, `max_attempts`, `base`, and `cap`. Each outcome is an integer HTTP status or the string `timeout`. Consume outcomes in order, up to max_attempts. Any status 200–299 succeeds. Only timeout and statuses 429, 500, 502, 503, 504 are retryable. Every other status stops with result `failed`. A retryable final allowed attempt stops with `exhausted`. Before retry number k (k starts at 1 after the first failed attempt), record delay `min(cap, base * 2**(k-1))`. Do not record a delay unless another attempt will run. Return `{attempts:int, delays:[int,...], result:"success"|"failed"|"exhausted"}`. Ignore unused outcomes. No actual sleeping or network calls.

## Examples

### Example 1: backoff is capped

Input to `solve`:
```json
{
  "outcomes": [
    503,
    503,
    200
  ],
  "max_attempts": 3,
  "base": 2,
  "cap": 3
}
```
Return:
```json
{
  "attempts": 3,
  "delays": [
    2,
    3
  ],
  "result": "success"
}
```

### Example 2: do not retry a client error

Input to `solve`:
```json
{
  "outcomes": [
    400,
    200
  ],
  "max_attempts": 2,
  "base": 1,
  "cap": 10
}
```
Return:
```json
{
  "attempts": 1,
  "delays": [],
  "result": "failed"
}
```

### Example 3: no delay after final failure

Input to `solve`:
```json
{
  "outcomes": [
    "timeout",
    504
  ],
  "max_attempts": 2,
  "base": 4,
  "cap": 20
}
```
Return:
```json
{
  "attempts": 2,
  "delays": [
    4
  ],
  "result": "exhausted"
}
```

## Constraints

- max_attempts is 1–10. outcomes contains at least max_attempts and at most 30 entries.
- Statuses are integers 100–599. base is 1–1000 and cap is 1–10000, in milliseconds.
- The exercise has no Retry-After header, jitter, or overall deadline.

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

- [Official documentation 1](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
