## Approach

The reference uses heapq with a monotonic insertion sequence. Each add or nonempty pop costs O(log n). The final pending sort costs O(n log n); storage is O(n). The judge verifies stable behavior, not heap use or complexity. This is a single-process simulation without worker execution or persistence.

## Python implementation

```python
import heapq

def solve(data: dict) -> dict:
    heap = []
    popped = []
    sequence = 0
    for action in data['actions']:
        if action['op'] == 'add':
            heapq.heappush(heap, (action['priority'], sequence, action['id']))
            sequence += 1
        else:
            popped.append(heapq.heappop(heap)[2] if heap else None)
    return {'popped': popped, 'pending': [entry[2] for entry in sorted(heap)]}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
