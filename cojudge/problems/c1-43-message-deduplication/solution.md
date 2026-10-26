## Approach

Use a processed-ID set and apply the effect only on the first committed delivery. Processing is expected O(D), with O(P log P) for sorted output and O(P + D) space. In a real consumer, the effect and dedup record need shared durable transaction semantics; an in-memory set is not sufficient after restart.

## Python implementation

```python
def solve(data: dict) -> dict:
    processed = set()
    total = data["total"]
    results = []
    for delivery in data["deliveries"]:
        key = delivery["id"]
        if key in processed:
            results.append("ack")
            continue
        if delivery["fail"] == "before":
            results.append("retry")
            continue
        total += delivery["amount"]
        processed.add(key)
        results.append("retry" if delivery["fail"] == "after" else "ack")
    return {"results": results, "total": total, "processed": sorted(processed)}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
