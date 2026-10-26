def solve(data: dict) -> dict:
    limits = []
    configured = 0
    for record in data['records']:
        if 'limit' not in record:
            limits.append(data['default'])
        else:
            value = record['limit']
            limits.append(value)
            if value is not None:
                configured += 1
    return {'limits': limits, 'configured': configured}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
