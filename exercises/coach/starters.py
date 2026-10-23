"""Controlled defects/missing features over the working reference templates.

This file is intentionally outside learner workspaces. Replacing complete named
functions keeps each task independent and makes the seeded difference auditable.
"""
import ast
from pathlib import Path
from textwrap import dedent

PATCHES = {
    'd01-bug': ('app/service.py', 'ordered', '''
def ordered(rows):
    return sorted(rows, key=lambda row: row['occurred_at'], reverse=True)
'''),
    'd01-feature': ('app/service.py', 'filtered', '''
def filtered(rows, category=None, min_cents=None):
    return list(rows)
'''),
    'd02-bug': ('app/service.py', 'transfer', '''
def transfer(store, request):
    source, target, amount = request.source, request.target, request.amount_cents
    if source not in store.accounts:
        raise HTTPException(404, 'Account not found')
    if store.accounts[source] < amount:
        raise HTTPException(409, 'Insufficient funds')
    store.accounts[source] -= amount
    if target not in store.accounts:
        raise HTTPException(404, 'Account not found')
    store.accounts[target] += amount
    item = {'id': f'tr-{len(store.transfers) + 1}', 'source': source, 'target': target, 'amount_cents': amount}
    store.transfers.append(item)
    return item
'''),
    'd02-feature': ('app/service.py', 'history', '''
def history(store, account):
    raise HTTPException(501, 'History is not implemented')
'''),
    'd03-bug': ('app/service.py', 'cashback', '''
def cashback(store, month, cap_cents):
    total = sum(round(row['amount_cents'] * 0.02) for row in monthly_rows(store, month) if row['kind'] == 'purchase')
    return {'cashback_cents': min(total, cap_cents) if cap_cents is not None else total}
'''),
    'd03-feature': ('app/service.py', 'cashback', '''
def cashback(store, month, cap_cents):
    total = sum(row['amount_cents'] * 2 // 100 for row in monthly_rows(store, month) if row['kind'] == 'purchase')
    return {'cashback_cents': total}
'''),
    'd04-bug': ('app/service.py', 'transaction_page', '''
def transaction_page(store, category, min_cents, page, page_size):
    start = (page - 1) * page_size
    all_rows = ordered(store.transactions)
    rows = filtered(all_rows[start:start + page_size], category, min_cents)
    total = len(filtered(all_rows, category, min_cents))
    return {'items': rows, 'total': total, 'page': page, 'page_size': page_size, 'has_next': start + page_size < total}
'''),
    'd04-feature': ('app/service.py', 'transaction_page', '''
def transaction_page(store, category, min_cents, page, page_size):
    rows = ordered(filtered(store.transactions, category, min_cents))
    start = (page - 1) * page_size
    return {'items': rows[start:start + page_size]}
'''),
    'd05-bug': ('app/service.py', 'spend', '''
def spend(store, month):
    return {'net_cents': sum(row['amount_cents'] for row in monthly_rows(store, month))}
'''),
    'd05-feature': ('app/service.py', 'categories', '''
def categories(store, month):
    raise HTTPException(501, 'Category summary is not implemented')
'''),
    'd06-bug': ('app/service.py', 'accounts', '''
def accounts(store):
    return {'items': [{'id': key, 'balance': amount} for key, amount in store.accounts.items()]}
'''),
    'd06-feature': ('app/models.py', 'Transfer', '''
class Transfer(BaseModel):
    source: str
    target: str
    amount_cents: int
'''),
    'd07-bug': ('app/service.py', 'accept_event', '''
def accept_event(store, event):
    store.accounts['checking'] += event.amount_cents
    result = {'event_id': event.event_id, 'amount_cents': event.amount_cents, 'accepted': True}
    store.events[event.event_id] = result
    return result
'''),
    'd07-feature': ('app/service.py', 'transfer_with_key', '''
def transfer_with_key(store, request, key):
    return transfer(store, request)
'''),
    'd08-bug': ('app/service.py', 'eligible', '''
def eligible(store, merchant_id):
    return [row for row in store.charges if row['merchant_id'] == merchant_id and row['status'] != 'refunded' and not row['settled']]
'''),
    'd08-feature': ('app/service.py', 'summary', '''
def summary(store, merchant_id, on):
    raise HTTPException(501, 'Daily merchant summary is not implemented')
'''),
    'd09-bug': ('app/rules.py', 'eligible', '''
def eligible(purchase):
    return purchase.active_member and purchase.amount_cents >= MINIMUM_CENTS and START <= purchase.at <= END
'''),
    'd09-feature': ('app/rules.py', 'quote', '''
def quote(purchase):
    raise HTTPException(501, 'Reward quote is not implemented')
'''),
    'd10-bug': ('app/service.py', 'reserve', '''
def reserve(store, request):
    for item in request.items:
        if item.sku not in store.products:
            raise HTTPException(404, 'Product not found')
        if store.products[item.sku]['available'] < item.quantity:
            raise HTTPException(409, 'Insufficient stock')
        store.products[item.sku]['available'] -= item.quantity
    result = {'id': f'r-{len(store.reservations) + 1}', 'status': 'active', 'items': [item.model_dump() for item in request.items]}
    store.reservations[result['id']] = result
    return result
'''),
    'd10-feature': ('app/service.py', 'cancel', '''
def cancel(store, reservation_id):
    raise HTTPException(501, 'Cancellation is not implemented')
'''),
}


def apply_starter(task_id: str, destination: Path):
    relative, name, replacement = PATCHES[task_id]
    path = destination / relative
    source = path.read_text()
    node = next(node for node in ast.parse(source).body if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == name)
    lines = source.splitlines(keepends=True)
    lines[node.lineno - 1:node.end_lineno] = [dedent(replacement).lstrip()]
    path.write_text(''.join(lines))
