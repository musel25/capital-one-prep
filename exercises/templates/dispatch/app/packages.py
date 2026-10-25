def weights_for_order(store, order):
    # Each physical unit ships in a separately labeled parcel.
    return [store.product(line['sku'])['weight_grams']
            for line in order['items'] for _ in range(line['quantity'])]


def billable_units(weights):
    return sum((weight + 499) // 500 for weight in weights)
