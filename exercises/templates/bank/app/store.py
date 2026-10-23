"""Fictitious in-memory fixtures. Restart the server to reset state."""
from copy import deepcopy

TRANSACTIONS = [
    {'id': 't01', 'occurred_at': '2026-10-01T08:00:00Z', 'category': 'groceries', 'amount_cents': 1999, 'kind': 'purchase', 'status': 'posted'},
    {'id': 't02', 'occurred_at': '2026-10-02T10:00:00-07:00', 'category': 'travel', 'amount_cents': 5000, 'kind': 'purchase', 'status': 'posted'},
    {'id': 't03', 'occurred_at': '2026-10-02T16:30:00Z', 'category': 'groceries', 'amount_cents': 1200, 'kind': 'purchase', 'status': 'posted'},
    {'id': 't04', 'occurred_at': '2026-10-02T16:30:00Z', 'category': 'dining', 'amount_cents': 3000, 'kind': 'purchase', 'status': 'pending'},
    {'id': 't05', 'occurred_at': '2026-10-03T09:00:00Z', 'category': 'adjustments', 'amount_cents': 499, 'kind': 'refund', 'status': 'posted', 'purchase_id': 't01'},
    {'id': 't06', 'occurred_at': '2026-10-02T16:30:00Z', 'category': 'groceries', 'amount_cents': 2500, 'kind': 'purchase', 'status': 'posted'},
    {'id': 't07', 'occurred_at': '2026-09-30T09:00:00Z', 'category': 'groceries', 'amount_cents': 2000, 'kind': 'purchase', 'status': 'posted'},
]


class Store:
    def __init__(self):
        self.transactions = deepcopy(TRANSACTIONS)
        self.accounts = {'checking': 100000, 'savings': 20000}
        self.transfers = []
        self.events = {}
        self.idempotency = {}
