## Approach

Process each call once with explicit closed, blocked-open, and half-open-probe paths. Time is O(C); working state is O(1), plus O(C) results. Production breakers must define which failures count, how concurrent probes are limited, and whether state is shared across processes.

## Python implementation

```python
def solve(data: dict) -> dict:
    state = "closed"
    failures = 0
    retry_at = None
    results = []
    for call in data["calls"]:
        now = call["at"]
        if state == "open" and now < retry_at:
            results.append({"mode": "blocked", "result": "blocked", "state": "open"})
            continue
        mode = "probe" if state == "open" else "closed"
        if call["ok"]:
            state, failures, retry_at = "closed", 0, None
            result = "success"
        else:
            failures += 1
            result = "failure"
            if mode == "probe" or failures >= data["threshold"]:
                state = "open"
                retry_at = now + data["cooldown"]
        results.append({"mode": mode, "result": result, "state": state})
    return {"results": results, "state": state, "failures": failures, "retry_at": retry_at}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
