## Approach

The reference uses a tuple key and Python stable sorting. It does not add an ID tie breaker. Time is O(n log n), and space is O(n). The judge verifies ordering. It cannot prove that a submission uses sorted or has this complexity. A production queue also needs a policy for updates and persistence.

## Python implementation

```python
def solve(data: dict) -> list[str]:
    ordered = sorted(data['tickets'], key=lambda ticket: (-ticket['priority'], ticket['created']))
    return [ticket['id'] for ticket in ordered]

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
