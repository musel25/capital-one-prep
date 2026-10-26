def solve(data: dict) -> dict:
    balance = data['balance']
    seen: dict[str, int] = {}
    status = []
    for event in data['events']:
        event_id, delta = event['id'], event['delta']
        if event_id not in seen:
            seen[event_id] = delta
            balance += delta
            status.append('applied')
        elif seen[event_id] == delta:
            status.append('duplicate')
        else:
            status.append('conflict')
    return {'status': status, 'balance': balance}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
