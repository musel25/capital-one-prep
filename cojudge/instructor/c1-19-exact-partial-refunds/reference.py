from dataclasses import dataclass

@dataclass
class Payment:
    charged: int
    refunded: int = 0

    @property
    def remaining(self) -> int:
        return self.charged - self.refunded

    def refund(self, cents: int) -> bool:
        if cents > self.remaining:
            return False
        self.refunded += cents
        return True

def solve(data: dict) -> dict:
    payments = {key: Payment(cents) for key, cents in data['payments'].items()}
    accepted = [payments[r['payment']].refund(r['cents']) for r in data['refunds']]
    return {'accepted': accepted, 'remaining': {key: p.remaining for key, p in payments.items()}}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
