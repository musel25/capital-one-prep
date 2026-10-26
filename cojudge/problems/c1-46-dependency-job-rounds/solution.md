## Approach

Scan unfinished jobs at each round and compare their dependency sets with completed jobs. Worst-case time is O(V × (V + E) + V² log V) for this small model; space is O(V + E). An indegree graph and ordered ready queue can scale better. Real schedulers also need failures, duration estimates, and resource limits.

## Python implementation

```python
def solve(data: dict) -> dict:
    dependencies = {job["id"]: set(job["depends"]) for job in data["jobs"]}
    pending = set(dependencies)
    completed = set()
    rounds = []
    while pending:
        ready = sorted(key for key in pending if dependencies[key] <= completed)
        if not ready:
            break
        selected = ready[:data["workers"]]
        rounds.append(selected)
        pending.difference_update(selected)
        completed.update(selected)
    return {"rounds": rounds, "blocked": sorted(pending), "has_cycle": bool(pending)}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
