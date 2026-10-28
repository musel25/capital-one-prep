## Reference solution

```python
def reserve_stock(stock, requests):
    remaining = dict(stock)
    accepted = []
    for request in requests:
        sku, quantity = request["sku"], request["quantity"]
        enough = sku in remaining and remaining[sku] >= quantity
        if enough:
            remaining[sku] -= quantity
        accepted.append(enough)
    return {"accepted": accepted, "stock": remaining}
```
