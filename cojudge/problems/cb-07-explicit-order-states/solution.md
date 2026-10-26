## Approach

The reference stores allowed transitions in a dictionary. Each action takes expected O(1) time; total time and output space are O(n). The judge checks transition behavior, not table use. This is a deterministic simulation. It does not test concurrent state changes or persistence.

## Review of the AI claim

The claim is incorrect under this contract. Use actions `["authorize", "authorize", "capture"]`. Expect `{"accepted": [true, false, true], "state": "CAPTURED"}`. Only `NEW + authorize` is allowed. The second request is rejected even though the order is already authorized. This model reports accepted transitions, not whether a requested state already holds.

## Provenance

This guided repair reuses the verified behavior contract and independent oracle from Engineering 50 problem 16. The starter, reading task, test plan, and AI review exercise form a new lesson.

## Python implementation

```python
class Order:
    TRANSITIONS = {
        ('NEW', 'authorize'): 'AUTHORIZED',
        ('NEW', 'cancel'): 'CANCELLED',
        ('AUTHORIZED', 'capture'): 'CAPTURED',
        ('AUTHORIZED', 'cancel'): 'CANCELLED',
        ('CAPTURED', 'refund'): 'REFUNDED',
    }

    def __init__(self):
        self.state = 'NEW'

    def apply(self, action: str) -> bool:
        next_state = self.TRANSITIONS.get((self.state, action))
        if next_state is None:
            return False
        self.state = next_state
        return True

def solve(data: dict) -> dict:
    order = Order()
    accepted = [order.apply(action) for action in data['actions']]
    return {'accepted': accepted, 'state': order.state}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
