def solve(data: dict) -> dict:
    balances = dict(data["balances"])
    committed = {}
    events = []
    results = []
    for op in data["payments"]:
        key = op["key"]
        payload = (op["from"], op["to"], op["amount"])
        if key in committed:
            results.append("replay" if committed[key] == payload else "conflict")
            continue
        source, target, amount = payload
        if balances[source] < amount:
            results.append("insufficient")
            continue
        staged = dict(balances)
        staged[source] -= amount
        if op["fail"] == "debit":
            results.append("failed")
            continue
        staged[target] += amount
        event = [key, source, target, amount]
        if op["fail"] == "outbox":
            results.append("failed")
            continue
        balances = staged
        committed[key] = payload
        events.append(event)
        results.append("ok")
    return {"results": results, "balances": balances, "events": events}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
