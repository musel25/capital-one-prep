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
