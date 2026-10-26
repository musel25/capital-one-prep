def solve(data: dict) -> dict:
    available = data["stock"]
    reservations = {}
    results = []
    for op in data["ops"]:
        now = op["at"]
        for item in reservations.values():
            if item["state"] == "held" and item["expires"] <= now:
                item["state"] = "expired"
                available += item["qty"]
        key = op["id"]
        existing = reservations.get(key)
        if op["op"] == "reserve":
            if existing is not None:
                same = existing["qty"] == op["qty"] and existing["ttl"] == op["ttl"]
                results.append(existing["state"] if same else "conflict")
            elif op["qty"] > available:
                results.append("insufficient")
            else:
                available -= op["qty"]
                reservations[key] = {"qty": op["qty"], "ttl": op["ttl"], "expires": now + op["ttl"], "state": "held"}
                results.append("held")
        elif existing is None:
            results.append("missing")
        else:
            if existing["state"] == "held":
                if op["op"] == "confirm":
                    existing["state"] = "confirmed"
                else:
                    existing["state"] = "released"
                    available += existing["qty"]
            results.append(existing["state"])
    return {"results": results, "available": available, "reservations": [[key, reservations[key]["state"]] for key in sorted(reservations)]}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
