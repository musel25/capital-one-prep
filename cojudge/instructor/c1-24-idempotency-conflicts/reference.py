def solve(data):
    cache = {}
    transfers = []
    out = []
    for request in data["requests"]:
        key, body = request["key"], request["body"]
        if key in cache:
            saved_body, result = cache[key]
            if body != saved_body:
                out.append({"status": 409, "body": {"error": "key_conflict"}, "replayed": False})
            else:
                out.append({"status": 201, "body": dict(result), "replayed": True})
        else:
            result = {"id": len(transfers) + 1, "to": body["to"], "amount": body["amount"]}
            transfers.append(dict(result))
            cache[key] = (dict(body), dict(result))
            out.append({"status": 201, "body": dict(result), "replayed": False})
    return {"responses": out, "transfers": transfers}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
