from copy import deepcopy


def products(store):
    return {'items': deepcopy(list(store.products.values()))}


def stock(store):
    return {'items': [{'sku': sku, 'available': amount} for sku, amount in sorted(store.available.items())]}
