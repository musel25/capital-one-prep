def solve(data: dict) -> dict:
    total = 0
    rejected = []
    for index, value in enumerate(data['values']):
        if type(value) is int and value >= 0:
            total += value
        else:
            rejected.append(index)
    return {'total': total, 'rejected': rejected}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
