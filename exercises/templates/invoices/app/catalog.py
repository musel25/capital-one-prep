from fastapi import HTTPException

PRODUCTS = {
    'notebook': {'sku': 'notebook', 'name': 'Pocket notebook', 'unit_cents': 999},
    'labels': {'sku': 'labels', 'name': 'Label sheet', 'unit_cents': 49},
    'clips': {'sku': 'clips', 'name': 'Clip pack', 'unit_cents': 105},
}


def product(sku):
    if sku not in PRODUCTS:
        raise HTTPException(404, 'Product not found')
    return PRODUCTS[sku]
