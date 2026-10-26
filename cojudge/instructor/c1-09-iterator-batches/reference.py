from itertools import islice

def solve(data: dict) -> list[list[int]]:
    values = iter(data['values'])
    batches = []
    while True:
        batch = list(islice(values, data['size']))
        if not batch:
            break
        batches.append(batch)
    return batches

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
