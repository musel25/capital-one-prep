## Approach

The reference processes the input in one pass. Time is O(n), and result storage is O(n). The output judge checks results. It cannot prove the requested Python technique. This is an in-memory exercise; it does not provide storage or concurrency control.

## Python implementation

```python
from datetime import datetime, timezone

def solve(data: dict) -> list[str]:
    result = []
    for text in data['timestamps']:
        instant = datetime.fromisoformat(text.replace('Z', '+00:00'))
        result.append(instant.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    return result

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
