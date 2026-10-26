def solve(data: dict) -> dict:
    replicas = {r["id"]: (r["version"], r["value"]) for r in data["replicas"]}
    results = []
    for op in data["ops"]:
        if op["op"] == "publish":
            previous = replicas[op["id"]][0]
            if op["version"] < previous:
                results.append("stale")
            elif op["version"] == previous:
                results.append("unchanged")
            else:
                replicas[op["id"]] = (op["version"], op["value"])
                results.append("applied")
        else:
            eligible = [key for key, (version, _) in replicas.items() if version >= op["min_version"]]
            if not eligible:
                results.append(None)
            else:
                key = min(eligible, key=lambda k: (-replicas[k][0], k))
                version, value = replicas[key]
                results.append({"id": key, "version": version, "value": value})
    return {"results": results, "replicas": [[key, *replicas[key]] for key in sorted(replicas)]}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
