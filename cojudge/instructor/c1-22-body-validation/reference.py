import re

def solve(data):
    out = []
    for body in data["bodies"]:
        if not isinstance(body, dict):
            out.append({"status": 400, "errors": ["body"]})
            continue
        errors = []
        account = body.get("account")
        amount = body.get("amount")
        note = body.get("note")
        if not isinstance(account, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,11}", account):
            errors.append("account")
        if type(amount) is not int or not 1 <= amount <= 10000:
            errors.append("amount")
        if note is not None and (not isinstance(note, str) or len(note) > 20):
            errors.append("note")
        if set(body) - {"account", "amount", "note"}:
            errors.append("unknown")
        if errors:
            out.append({"status": 422, "errors": errors})
        else:
            out.append({"status": 201, "body": {"account": account, "amount": amount, "note": note}})
    return out

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
