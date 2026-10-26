class Ledger:
    def __init__(self, balances: dict[str, int]):
        self.balances = balances.copy()

    def apply_batch(self, transfers: list[dict]) -> bool:
        trial = self.balances.copy()
        for transfer in transfers:
            source, target, cents = transfer['from'], transfer['to'], transfer['cents']
            if trial[source] < cents:
                return False
            trial[source] -= cents
            trial[target] += cents
        self.balances = trial
        return True

def solve(data: dict) -> dict:
    ledger = Ledger(data['accounts'])
    accepted = [ledger.apply_batch(batch) for batch in data['batches']]
    return {'accepted': accepted, 'balances': ledger.balances}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
