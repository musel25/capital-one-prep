def solve(data: dict) -> dict:
    entries = {}
    results = []
    for op in data["ops"]:
        now = op["at"]
        for key in list(entries):
            if entries[key][1] <= now:
                del entries[key]
        key = op["key"]
        if op["op"] == "put":
            if op["ttl"] > 0:
                entries[key] = (op["value"], now + op["ttl"])
            else:
                entries.pop(key, None)
            results.append("stored")
        elif op["op"] == "get":
            results.append(entries[key][0] if key in entries else None)
        else:
            results.append(key in entries)
            entries.pop(key, None)
    return {"results": results, "keys": sorted(entries)}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
