from datetime import datetime
from fastapi import HTTPException


def instant(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def ordered(rows):
    return sorted(rows, key=lambda row: (-instant(row['occurred_at']).timestamp(), row['id']))


def filtered(rows, category=None, min_cents=None):
    return [row for row in rows if (category is None or row['category'] == category) and (min_cents is None or row['amount_cents'] >= min_cents)]


def transaction_page(store, category, min_cents, page, page_size):
    rows = ordered(filtered(store.transactions, category, min_cents))
    start = (page - 1) * page_size
    return {'items': rows[start:start + page_size], 'total': len(rows), 'page': page, 'page_size': page_size, 'has_next': start + page_size < len(rows)}


def transfer(store, request):
    source, target, amount = request.source, request.target, request.amount_cents
    if source not in store.accounts or target not in store.accounts:
        raise HTTPException(404, 'Account not found')
    if store.accounts[source] < amount:
        raise HTTPException(409, 'Insufficient funds')
    store.accounts[source] -= amount
    store.accounts[target] += amount
    item = {'id': f'tr-{len(store.transfers) + 1}', 'source': source, 'target': target, 'amount_cents': amount}
    store.transfers.append(item)
    return item


def transfer_with_key(store, request, key):
    payload = request.model_dump()
    if key and key in store.idempotency:
        previous = store.idempotency[key]
        if previous['payload'] != payload:
            raise HTTPException(409, 'Key was used with a different payload')
        return previous['result']
    result = transfer(store, request)
    if key:
        store.idempotency[key] = {'payload': payload, 'result': result}
    return result


def history(store, account):
    if account not in store.accounts:
        raise HTTPException(404, 'Account not found')
    return {'items': [
        {'transfer_id': row['id'], 'amount_cents': -row['amount_cents'] if row['source'] == account else row['amount_cents']}
        for row in store.transfers if account in (row['source'], row['target'])
    ]}


def monthly_rows(store, month):
    return [row for row in store.transactions if row['occurred_at'][:7] == month and row['status'] == 'posted']


def cashback(store, month, cap_cents):
    total = sum(row['amount_cents'] * 2 // 100 for row in monthly_rows(store, month) if row['kind'] == 'purchase')
    return {'cashback_cents': min(total, cap_cents) if cap_cents is not None else total}


def spend(store, month):
    return {'net_cents': sum(row['amount_cents'] * (-1 if row['kind'] == 'refund' else 1) for row in monthly_rows(store, month))}


def categories(store, month):
    by_id = {row['id']: row for row in store.transactions}
    totals = {}
    for row in monthly_rows(store, month):
        category = by_id[row['purchase_id']]['category'] if row['kind'] == 'refund' else row['category']
        totals[category] = totals.get(category, 0) + row['amount_cents'] * (-1 if row['kind'] == 'refund' else 1)
    return {'items': [{'category': category, 'net_cents': amount} for category, amount in sorted(totals.items())]}


def accounts(store):
    return {'items': [{'id': key, 'balance_cents': amount} for key, amount in store.accounts.items()]}


def accept_event(store, event):
    if event.event_id in store.events:
        result = store.events[event.event_id]
        if result['amount_cents'] != event.amount_cents:
            raise HTTPException(409, 'Event payload conflict')
        return result
    store.accounts['checking'] += event.amount_cents
    result = {'event_id': event.event_id, 'amount_cents': event.amount_cents, 'accepted': True}
    store.events[event.event_id] = result
    return result
