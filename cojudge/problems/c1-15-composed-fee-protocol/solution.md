## Approach

The reference uses a Protocol, two policy classes, and a Calculator that holds a policy. It selects the policy once. Time is O(n), and result space is O(n). The output judge verifies fee calculations, not Protocol, composition, or polymorphism. The policy is a constructed exercise, not a pricing recommendation.

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
