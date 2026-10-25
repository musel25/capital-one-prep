from copy import deepcopy
from fastapi import HTTPException
from .packages import weights_for_order
from .quotes import quote
from .events import record


def ship(store, request):
    order = store.order(request.order_id)
    if order['status'] != 'reserved':
        raise HTTPException(409, 'Order must be reserved before shipment')
    cost = quote(weights_for_order(store, order), request.service, request.signature)
    shipment = {'id': f's-{len(store.shipments) + 1}', 'order_id': order['id'],
                'status': 'label_created', 'service': request.service, **cost}
    store.shipments[shipment['id']] = shipment
    order['status'] = 'shipped'
    record(store, order['id'], 'shipped', {'shipment_id': shipment['id'], 'total_cents': cost['total_cents']})
    return deepcopy(shipment)
