from datetime import date

from fastapi import HTTPException

from .accounts import find_subscription
from .catalog import PLANS


def quote(accounts, subscription_id, request):
    subscription = find_subscription(accounts, subscription_id)
    target = PLANS.get(request.target_plan)
    if target is None:
        raise HTTPException(404, 'Plan not found')
    if subscription['status'] != 'active':
        raise HTTPException(409, 'Subscription is not active')
    difference = target['monthly_cents'] - PLANS[subscription['plan_id']]['monthly_cents']
    if difference < 0:
        raise HTTPException(409, 'Downgrades are scheduled separately')
    start = date.fromisoformat(subscription['period_start'])
    end = date.fromisoformat(subscription['period_end'])
    if not start <= request.effective_on <= end:
        raise HTTPException(422, 'Effective date must be within the current period')
    cycle_days = (end - start).days
    remaining_days = (end - request.effective_on).days
    uncapped = difference * remaining_days // cycle_days
    charge = uncapped if request.cap_cents is None else min(uncapped, request.cap_cents)
    return {
        'subscription_id': subscription_id,
        'target_plan': request.target_plan,
        'effective_on': request.effective_on.isoformat(),
        'cycle_days': cycle_days,
        'remaining_days': remaining_days,
        'uncapped_cents': uncapped,
        'charge_cents': charge,
    }
