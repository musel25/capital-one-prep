def solve(data):
    records = [dict(row) for row in data["records"]]
    out = []
    for action in data["actions"]:
        if action["op"] == "insert":
            records.append(dict(action["record"]))
            continue
        after = action["after"]
        eligible = sorted((r for r in records if after is None or (r["ts"], r["id"]) > tuple(after)), key=lambda r: (r["ts"], r["id"]))
        selected = eligible[:action["limit"]]
        more = len(eligible) > len(selected)
        cursor = [selected[-1]["ts"], selected[-1]["id"]] if more else None
        out.append({"ids": [r["id"] for r in selected], "next": cursor})
    return out

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
