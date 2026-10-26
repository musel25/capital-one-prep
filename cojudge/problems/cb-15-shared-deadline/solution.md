## Approach

Keep three counters and stop at the first unsuccessful step. Each step consumes only its actual completed duration or its bounded wait. Time is O(s), with O(1) extra space. The model is sequential and excludes cancellation overhead. It cannot demonstrate live network timing guarantees.

## Review of the AI claim

The claim is incorrect. For `{"budget": 0, "steps": [{"duration": 0, "timeout": 1, "outcome": "ok"}]}`, expect `{"result": "deadline", "elapsed": 0, "completed": 0, "started": 0}`. The start guard is a separate rule from how much time a started operation consumes. With the same zero budget and no steps, the result is success with all counters zero.

## Provenance

This guided repair reuses the verified behavior contract and independent oracle from Engineering 50 problem 27. The starter, reading task, test plan, and AI review exercise form a new lesson.

## Python implementation

```python
def solve(data):
    elapsed = completed = started = 0
    for step in data["steps"]:
        remaining = data["budget"] - elapsed
        if remaining <= 0:
            return {"result": "deadline", "elapsed": elapsed, "completed": completed, "started": started}
        started += 1
        allowance = min(step["timeout"], remaining)
        if step["duration"] > allowance:
            elapsed += allowance
            result = "deadline" if allowance == remaining else "timeout"
            return {"result": result, "elapsed": elapsed, "completed": completed, "started": started}
        elapsed += step["duration"]
        if step["outcome"] == "error":
            return {"result": "error", "elapsed": elapsed, "completed": completed, "started": started}
        completed += 1
    return {"result": "success", "elapsed": elapsed, "completed": completed, "started": started}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
