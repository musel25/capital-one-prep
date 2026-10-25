from fastapi import HTTPException


class Accounts:
    def __init__(self):
        self.subscriptions = {
            'sub-100': {'id': 'sub-100', 'customer': 'Fern Studio', 'plan_id': 'basic', 'status': 'active', 'period_start': '2026-10-01', 'period_end': '2026-11-01'},
            'sub-200': {'id': 'sub-200', 'customer': 'Harbor Collective', 'plan_id': 'plus', 'status': 'active', 'period_start': '2026-10-15', 'period_end': '2026-11-15'},
            'sub-300': {'id': 'sub-300', 'customer': 'Closed Workshop', 'plan_id': 'basic', 'status': 'cancelled', 'period_start': '2026-10-01', 'period_end': '2026-11-01'},
        }


def find_subscription(accounts, subscription_id):
    if subscription_id not in accounts.subscriptions:
        raise HTTPException(404, 'Subscription not found')
    return accounts.subscriptions[subscription_id]
