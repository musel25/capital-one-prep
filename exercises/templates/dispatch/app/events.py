from copy import deepcopy


def record(store, order_id, kind, detail):
    event = {'sequence': len(store.events) + 1, 'order_id': order_id,
             'kind': kind, 'detail': deepcopy(detail)}
    store.events.append(event)
    return deepcopy(event)


def history(store, order_id=None):
    if order_id is not None:
        store.order(order_id)
    return {'items': deepcopy([e for e in store.events if order_id is None or e['order_id'] == order_id])}
