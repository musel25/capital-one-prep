from copy import deepcopy
from fastapi import APIRouter
from .models import OrderRequest, QuoteRequest, ShipmentRequest
from .catalog import products, stock
from .events import history
from .orders import create, cancel
from .quotes import quote
from .rates import rate_cards
from .shipments import ship
from .tracking import lookup


def api(store):
    router = APIRouter(prefix='/api')

    @router.get('/products')
    def catalog():
        return products(store)

    @router.get('/inventory')
    def inventory():
        return stock(store)

    @router.get('/rates')
    def rates():
        return rate_cards()

    @router.get('/orders')
    def orders():
        return {'items': deepcopy(list(store.orders.values()))}

    @router.get('/orders/{order_id}')
    def order(order_id: str):
        return deepcopy(store.order(order_id))

    @router.post('/orders', status_code=201)
    def new_order(request: OrderRequest):
        return create(store, request)

    @router.post('/orders/{order_id}/cancel')
    def cancel_order(order_id: str):
        return cancel(store, order_id)

    @router.post('/quotes')
    def preview(request: QuoteRequest):
        return quote(request.weights_grams, request.service, request.signature)

    @router.post('/shipments', status_code=201)
    def shipment(request: ShipmentRequest):
        return ship(store, request)

    @router.get('/shipments/{shipment_id}')
    def tracking(shipment_id: str):
        return lookup(store, shipment_id)

    @router.get('/events')
    def events():
        return history(store)

    @router.get('/orders/{order_id}/events')
    def order_events(order_id: str):
        return history(store, order_id)

    return router
