from copy import deepcopy

CHARGES = [
    {'id': 's01', 'merchant_id': 'fern', 'date': '2026-10-30', 'gross_cents': 10000, 'fee_cents': 300, 'status': 'captured', 'settled': False},
    {'id': 's02', 'merchant_id': 'fern', 'date': '2026-10-30', 'gross_cents': 4000, 'fee_cents': 120, 'status': 'refunded', 'settled': False},
    {'id': 's03', 'merchant_id': 'fern', 'date': '2026-10-30', 'gross_cents': 6000, 'fee_cents': 180, 'status': 'captured', 'settled': False},
    {'id': 's04', 'merchant_id': 'fern', 'date': '2026-10-30', 'gross_cents': 8000, 'fee_cents': 240, 'status': 'authorized', 'settled': False},
    {'id': 's05', 'merchant_id': 'harbor', 'date': '2026-10-30', 'gross_cents': 1200, 'fee_cents': 36, 'status': 'captured', 'settled': False},
    {'id': 's06', 'merchant_id': 'fern', 'date': '2026-10-30', 'gross_cents': 2000, 'fee_cents': 60, 'status': 'captured', 'settled': True},
]


class Store:
    def __init__(self):
        self.charges = deepcopy(CHARGES)
