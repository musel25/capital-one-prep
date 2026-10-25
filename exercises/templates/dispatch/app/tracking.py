from copy import deepcopy
from fastapi import HTTPException


def lookup(store, shipment_id):
    if shipment_id not in store.shipments:
        raise HTTPException(404, 'Shipment not found')
    shipment = store.shipments[shipment_id]
    return {'shipment': deepcopy(shipment),
            'events': deepcopy([e for e in store.events if e['order_id'] == shipment['order_id']])}
