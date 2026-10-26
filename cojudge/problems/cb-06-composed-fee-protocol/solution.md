## Approach

The reference uses a Protocol, two policy classes, and a Calculator that holds a policy. It selects the policy once. Time is O(n), and result space is O(n). The output judge verifies fee calculations, not Protocol, composition, or polymorphism. The policy is a constructed exercise, not a pricing recommendation.

## Review of the AI claim

The claim is incorrect. For `{"policy": {"kind": "flat", "cents": 7}, "amounts": [0]}`, expect `[{"fee": 7, "total": 7}]`. A rate policy with `bps = 7` on the same amount returns `[{"fee": 0, "total": 0}]`. The policy contract determines the fee. The calculator must not impose a universal zero-amount shortcut.

## Provenance

This guided repair reuses the verified behavior contract and independent oracle from Engineering 50 problem 15. The starter, reading task, test plan, and AI review exercise form a new lesson.

## Python implementation

```python
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

```
