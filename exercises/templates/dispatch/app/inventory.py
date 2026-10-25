from fastapi import HTTPException


def quantities(lines):
    totals = {}
    for line in lines:
        totals[line['sku']] = totals.get(line['sku'], 0) + line['quantity']
    return totals


def reserve(store, lines):
    totals = quantities(lines)
    for sku, count in totals.items():
        store.product(sku)
        if store.available[sku] < count:
            raise HTTPException(409, 'Insufficient stock')
    for sku, count in totals.items():
        store.available[sku] -= count


def release(store, lines):
    for sku, count in quantities(lines).items():
        store.available[sku] += count
