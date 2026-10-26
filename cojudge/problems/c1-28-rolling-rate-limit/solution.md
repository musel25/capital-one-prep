## Approach

Maintain a deque for each user. Each accepted timestamp is appended once and removed at most once, giving O(e) total time. Active histories use O(u * limit) space for u users, plus output. The Java oracle independently filters timestamp lists. This does not test concurrent rate-limit enforcement.

## Python implementation

```python
from collections import defaultdict, deque

def solve(data):
    accepted = defaultdict(deque)
    out = []
    for event in data["events"]:
        now = event["time"]
        queue = accepted[event["user"]]
        while queue and queue[0] <= now - data["window"]:
            queue.popleft()
        allowed = len(queue) < data["limit"]
        if allowed:
            queue.append(now)
        out.append({"allowed": allowed, "remaining": data["limit"] - len(queue), "retry_after": 0 if allowed else queue[0] + data["window"] - now})
    return out

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
