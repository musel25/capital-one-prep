class Account:
    def __init__(self, balance: int):
        self._balance = balance

    @property
    def balance(self) -> int:
        return self._balance

    def deposit(self, cents: int) -> bool:
        self._balance += cents
        return True

    def withdraw(self, cents: int) -> bool:
        if cents > self._balance:
            return False
        self._balance -= cents
        return True

def solve(data: dict) -> dict:
    account = Account(data['balance'])
    accepted = []
    for action in data['actions']:
        method = account.deposit if action['op'] == 'deposit' else account.withdraw
        accepted.append(method(action['cents']))
    return {'accepted': accepted, 'balance': account.balance}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
