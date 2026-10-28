An inventory service must accept reservations without selling stock that is not available.

Implement `reserve_stock(stock, requests)`. `stock` maps SKUs to available quantities. Each request has `sku` and `quantity`. Process reservations in request order.

Accept only when the SKU exists and the requested quantity is no greater than its remaining stock. Subtract stock only on success. Reject unknown SKUs without adding them.

Return `{'accepted': [...], 'stock': {...}}` with one boolean per request. Include every original SKU in the final stock, including zero balances. Empty inputs are valid.

**Constraints:**

- 0–300 SKUs and 0–300 requests. All required fields are present.
- SKU names are nonempty ASCII strings of at most 80 characters.
- Stock quantities are integers from 0 to 1000000000; requested quantities are integers from 1 to 1000000000.
- Do not change input objects or their nested values. Each call starts with fresh state.
