from copy import deepcopy
from fastapi import HTTPException
from .fixtures import PRODUCTS, AVAILABLE, ORDERS


class Store:
    def __init__(self):
        self.products = deepcopy(PRODUCTS)
        self.available = dict(AVAILABLE)
        self.orders = {o['id']: deepcopy(o) for o in ORDERS}
        self.shipments = {}
        self.events = []

    def order(self, order_id):
        if order_id not in self.orders:
            raise HTTPException(404, 'Order not found')
        return self.orders[order_id]

    def product(self, sku):
        if sku not in self.products:
            raise HTTPException(404, 'Product not found')
        return self.products[sku]
