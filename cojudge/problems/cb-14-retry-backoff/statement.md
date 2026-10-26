# 14. Separate failure classification from retry scheduling

[Back to the course list](/?course=capital-one-codebase-practice)

**Level 4 · Medium · About 35 minutes**

**Before this problem:** Exercise 13. Follow an ordered list of outcomes and a retry counter.

## Learn first

The retry loop classifies one outcome before it decides whether another attempt can run. The starter retries a class of failure that must stop. Your objective is to locate that policy decision while preserving attempt counts and delay placement.

A retry policy needs three decisions: which failures are temporary, how many attempts are allowed, and how long to wait between attempts. Retrying every failure can repeat a permanent error and overload a service. Exponential backoff increases delays after repeated temporary failures. A cap bounds each delay. An attempt limit includes the first request, so three attempts allow at most two waits. Production clients often add random jitter and honor server guidance. This exercise excludes both to make results deterministic. Its retry set is an explicit local policy. Apply it to an operation that is safe to repeat, such as a read or a protected write.

### Worked trace

Use outcomes `[503, "timeout", 204, 500]`, `max_attempts = 4`, `base = 3`, and `cap = 5`. Attempt 1 records delay `3`. Attempt 2 records delay `5`. Attempt 3 succeeds. Expect `{"attempts": 3, "delays": [3, 5], "result": "success"}`. The final 500 is unused. A delay belongs between attempts, not after the last outcome that the program consumes.

### Read the existing code

In `solve`, inspect `index`, `attempts`, `retryable`, and `delays`. Follow the return paths in order: success, non-retryable failure, and exhausted attempts. Then inspect delay construction. Mark which branch determines the error class and which branch determines whether capacity remains for another call.

## Your task

### Scoped repair

Repair only the retryable-outcome classification. Preserve the exact allowlist, 200–299 success range, attempt limit, exponential delay sequence, and cap. Keep `failed` distinct from `exhausted`. Do not add jitter, Retry-After handling, sleeping, real transport, or an overall deadline. This task supplies an explicit policy rather than a universal HTTP rule.

### Required behavior

Input fields are `outcomes`, `max_attempts`, `base`, and `cap`. Each outcome is an integer HTTP status or the string `timeout`. Consume outcomes in order, up to max_attempts. Any status 200–299 succeeds. Only timeout and statuses 429, 500, 502, 503, 504 are retryable. Every other status stops with result `failed`. A retryable final allowed attempt stops with `exhausted`. Before retry number k (k starts at 1 after the first failed attempt), record delay `min(cap, base * 2**(k-1))`. Do not record a delay unless another attempt will run. Return `{attempts:int, delays:[int,...], result:"success"|"failed"|"exhausted"}`. Ignore unused outcomes. No actual sleeping or network calls.

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

[Full sequence and local pytest labs](https://github.com/musel25/capital-one-prep/blob/main/codebase_labs/README.md). Then open [exercise 15](/problems/cb-15-shared-deadline).

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
