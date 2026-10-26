## Approach

Walk the outcome sequence until success, permanent failure, or the attempt limit. Append only delays that precede an actual retry. Time and output space are O(a) for a attempts. A production policy also considers idempotency, server hints, jitter, and a total deadline.

## Review of the AI claim

The claim is correct. For `outcomes = [501, 204]`, `max_attempts = 2`, `base = 4`, and `cap = 9`, expect `{"attempts": 1, "delays": [], "result": "failed"}`. This is an independent counterexample to the broader claim that all 5xx responses should retry. Changing only the first status to 502 gives two attempts, delay `[4]`, and success. The distinction comes from the explicit allowlist.

## Provenance

This guided repair reuses the verified behavior contract and independent oracle from Engineering 50 problem 26. The starter, reading task, test plan, and AI review exercise form a new lesson.

## Python implementation

```python
def solve(data):
    delays = []
    for index in range(data["max_attempts"]):
        outcome = data["outcomes"][index]
        attempts = index + 1
        if isinstance(outcome, int) and 200 <= outcome < 300:
            return {"attempts": attempts, "delays": delays, "result": "success"}
        retryable = outcome == "timeout" or outcome in (429, 500, 502, 503, 504)
        if not retryable:
            return {"attempts": attempts, "delays": delays, "result": "failed"}
        if attempts == data["max_attempts"]:
            return {"attempts": attempts, "delays": delays, "result": "exhausted"}
        delays.append(min(data["cap"], data["base"] * 2 ** index))

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
