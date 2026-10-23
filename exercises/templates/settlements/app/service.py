from fastapi import HTTPException


def eligible(store, merchant_id):
    return [row for row in store.charges if row['merchant_id'] == merchant_id and row['status'] == 'captured' and not row['settled']]


def summary(store, merchant_id, on):
    rows = [row for row in eligible(store, merchant_id) if row['date'] == on.isoformat()]
    gross = sum(row['gross_cents'] for row in rows)
    fees = sum(row['fee_cents'] for row in rows)
    return {'merchant_id': merchant_id, 'date': on.isoformat(), 'count': len(rows), 'gross_cents': gross, 'fees_cents': fees, 'net_cents': gross - fees}
