def solve(data: dict) -> list[str]:
    ordered = sorted(data['tickets'], key=lambda ticket: (-ticket['priority'], ticket['created']))
    return [ticket['id'] for ticket in ordered]

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
