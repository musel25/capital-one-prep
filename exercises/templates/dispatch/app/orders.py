from copy import deepcopy
from fastapi import HTTPException
from .inventory import reserve, release
from .events import record


def create(store, request):
    lines = [line.model_dump() for line in request.items]
    reserve(store, lines)
    order = {'id': f'o-{len(store.orders) + 1}', 'customer': request.customer,
             'status': 'reserved', 'items': lines}
    store.orders[order['id']] = order
    record(store, order['id'], 'reserved', {'items': lines})
    return deepcopy(order)


def cancel(store, order_id):
    order = store.order(order_id)
    if order['status'] == 'cancelled':
        return deepcopy(order)
    if order['status'] != 'reserved':
        raise HTTPException(409, 'Only reserved orders can be cancelled')
    release(store, order['items'])
    order['status'] = 'cancelled'
    record(store, order_id, 'cancelled', {'items': order['items']})
    return deepcopy(order)
