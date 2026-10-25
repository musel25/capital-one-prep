"""Available counts already exclude the reservations in ORDERS."""
PRODUCTS = {'cable': {'sku': 'cable', 'name': 'USB cable', 'weight_grams': 250},
            'dock': {'sku': 'dock', 'name': 'Laptop dock', 'weight_grams': 750}}
AVAILABLE = {'cable': 5, 'dock': 4}
ORDERS = [
    {'id': 'o-1', 'customer': 'Jo', 'status': 'reserved', 'items': [{'sku': 'cable', 'quantity': 2}]},
    {'id': 'o-2', 'customer': 'Lee', 'status': 'reserved', 'items': [{'sku': 'dock', 'quantity': 1}]},
    {'id': 'o-3', 'customer': 'Kai', 'status': 'shipped', 'items': [{'sku': 'cable', 'quantity': 1}]},
]
