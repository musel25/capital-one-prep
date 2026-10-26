def solve(data: dict) -> dict:
    messages = {key: {"token": 0, "until": 0, "done": False} for key in data["messages"]}
    results = []
    for op in data["ops"]:
        now = op["at"]
        if op["op"] == "receive":
            chosen = next((key for key, m in messages.items() if not m["done"] and m["until"] <= now), None)
            if chosen is None:
                results.append(None)
            else:
                m = messages[chosen]
                m["token"] += 1
                m["until"] = now + data["timeout"]
                results.append({"id": chosen, "token": m["token"]})
        else:
            m = messages.get(op["id"])
            accepted = m is not None and not m["done"] and m["token"] > 0 and m["token"] == op["token"] and now < m["until"]
            if accepted:
                m["done"] = True
            results.append(accepted)
    return {"results": results, "pending": [key for key, m in messages.items() if not m["done"]]}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
