RATES = {'standard': {'base_cents': 100, 'unit_cents': 40},
         'express': {'base_cents': 200, 'unit_cents': 75}}
SIGNATURE_CENTS = 100


def rate_cards():
    return {'items': [{'service': name, **rate} for name, rate in RATES.items()],
            'unit_grams': 500, 'signature_cents_per_shipment': SIGNATURE_CENTS}
