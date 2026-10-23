from datetime import datetime, timezone
from fastapi import HTTPException

START = datetime(2026, 10, 30, tzinfo=timezone.utc)
END = datetime(2026, 11, 1, tzinfo=timezone.utc)
MINIMUM_CENTS = 5000


def eligible(purchase):
    return purchase.active_member and purchase.amount_cents >= MINIMUM_CENTS and START <= purchase.at < END


def quote(purchase):
    qualifies = eligible(purchase)
    return {'eligible': qualifies, 'reward_cents': min(purchase.amount_cents * 5 // 100, 500) if qualifies else 0}
