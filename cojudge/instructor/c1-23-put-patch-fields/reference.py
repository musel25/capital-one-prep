def solve(data):
    state = dict(data["initial"])
    out = []
    for request in data["requests"]:
        body = request["body"]
        valid = isinstance(body, dict)
        if valid:
            valid = not (set(body) - {"name", "email"})
            valid = valid and (request["method"] != "PUT" or "name" in body)
            valid = valid and ("name" not in body or (isinstance(body["name"], str) and 1 <= len(body["name"]) <= 20))
            valid = valid and ("email" not in body or body["email"] is None or (isinstance(body["email"], str) and len(body["email"]) <= 30))
        if not valid:
            out.append({"status": 422, "body": {"error": "invalid"}})
            continue
        if request["method"] == "PUT":
            state = {"name": body["name"], "email": body.get("email")}
        else:
            for key in ("name", "email"):
                if key in body:
                    state[key] = body[key]
        out.append({"status": 200, "body": dict(state)})
    return {"responses": out, "state": state}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
