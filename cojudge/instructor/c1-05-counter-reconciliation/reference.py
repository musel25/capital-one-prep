from collections import Counter

def solve(data: dict) -> dict:
    expected = Counter(data['expected'])
    observed = Counter(data['observed'])
    def rows(counts):
        return [{'id': key, 'count': counts[key]} for key in sorted(counts)]
    return {'missing': rows(expected - observed), 'extra': rows(observed - expected)}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
