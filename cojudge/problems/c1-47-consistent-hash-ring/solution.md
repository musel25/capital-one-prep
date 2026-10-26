## Approach

Keep sorted hash points and mappings between points and node IDs. Lookup is O(log N); list insert and removal are O(N). Space is O(N + O) including results. Real rings need a stable hash function, collision policy, virtual nodes, and migration controls. This output judge cannot certify binary-search complexity.

## Python implementation

```python
from bisect import bisect_left, insort

def solve(data: dict) -> dict:
    points = sorted(node["hash"] for node in data["nodes"])
    owners = {node["hash"]: node["id"] for node in data["nodes"]}
    by_id = {node["id"]: node["hash"] for node in data["nodes"]}
    results = []
    for op in data["ops"]:
        if op["op"] == "lookup":
            if not points:
                results.append(None)
            else:
                index = bisect_left(points, op["hash"])
                results.append(owners[points[index % len(points)]])
        elif op["op"] == "add":
            insort(points, op["hash"])
            owners[op["hash"]] = op["id"]
            by_id[op["id"]] = op["hash"]
            results.append("added")
        else:
            key = op["id"]
            results.append(key in by_id)
            if key in by_id:
                point = by_id.pop(key)
                points.remove(point)
                del owners[point]
    return {"results": results, "ring": [[point, owners[point]] for point in points]}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
