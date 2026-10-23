class Store:
    def __init__(self):
        self.products = {'dock': {'sku': 'dock', 'available': 5, 'price_cents': 4000}, 'cable': {'sku': 'cable', 'available': 10, 'price_cents': 1200}}
        self.reservations = {}
