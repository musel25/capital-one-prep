from dataclasses import dataclass
from typing import Protocol

class FeePolicy(Protocol):
    def fee(self, amount: int) -> int: ...

@dataclass
class FlatFee:
    cents: int
    def fee(self, amount: int) -> int:
        return self.cents

@dataclass
class RateFee:
    bps: int
    def fee(self, amount: int) -> int:
        return (amount * self.bps + 9999) // 10000

class Calculator:
    def __init__(self, policy: FeePolicy):
        self.policy = policy
    def quote(self, amount: int) -> dict:
        fee = self.policy.fee(amount)
        return {'fee': fee, 'total': amount + fee}

def solve(data: dict) -> list[dict]:
    raw = data['policy']
    policy: FeePolicy = FlatFee(raw['cents']) if raw['kind'] == 'flat' else RateFee(raw['bps'])
    calculator = Calculator(policy)
    return [calculator.quote(amount) for amount in data['amounts']]

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
