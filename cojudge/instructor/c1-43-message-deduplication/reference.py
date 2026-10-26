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
