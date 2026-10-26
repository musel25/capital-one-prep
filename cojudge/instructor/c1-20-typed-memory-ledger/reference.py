from dataclasses import dataclass
from typing import TypedDict

Transfer = TypedDict('Transfer', {'id': str, 'from': str, 'to': str, 'cents': int})

@dataclass
class Account:
    balance: int

    def debit(self, cents: int) -> bool:
        if cents > self.balance:
            return False
        self.balance -= cents
        return True

    def credit(self, cents: int) -> None:
        self.balance += cents

class Ledger:
    def __init__(self, balances: dict[str, int]):
        self.accounts = {key: Account(value) for key, value in balances.items()}
        self.seen: dict[str, tuple[str, str, int]] = {}

    def apply(self, event: Transfer) -> str:
        identifier = event['id']
        payload = (event['from'], event['to'], event['cents'])
        if identifier in self.seen:
            return 'duplicate' if self.seen[identifier] == payload else 'conflict'
        self.seen[identifier] = payload
        source, target, cents = payload
        if not self.accounts[source].debit(cents):
            return 'insufficient'
        self.accounts[target].credit(cents)
        return 'applied'

def solve(data: dict) -> dict:
    ledger = Ledger(data['accounts'])
    status = [ledger.apply(event) for event in data['events']]
    return {'status': status, 'balances': {key: account.balance for key, account in ledger.accounts.items()}}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)
