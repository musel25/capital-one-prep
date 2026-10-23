from fastapi import HTTPException


def reserve(store, request):
    quantities = {}
    for item in request.items:
        quantities[item.sku] = quantities.get(item.sku, 0) + item.quantity
    for sku, quantity in quantities.items():
        if sku not in store.products:
            raise HTTPException(404, 'Product not found')
        if store.products[sku]['available'] < quantity:
            raise HTTPException(409, 'Insufficient stock')
    for sku, quantity in quantities.items():
        store.products[sku]['available'] -= quantity
    result = {'id': f'r-{len(store.reservations) + 1}', 'status': 'active', 'items': [{'sku': sku, 'quantity': quantity} for sku, quantity in quantities.items()]}
    store.reservations[result['id']] = result
    return result


def cancel(store, reservation_id):
    if reservation_id not in store.reservations:
        raise HTTPException(404, 'Reservation not found')
    reservation = store.reservations[reservation_id]
    if reservation['status'] == 'active':
        for item in reservation['items']:
            store.products[item['sku']]['available'] += item['quantity']
        reservation['status'] = 'canceled'
    return reservation
