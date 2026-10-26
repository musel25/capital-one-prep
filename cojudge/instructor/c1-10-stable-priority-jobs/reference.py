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
