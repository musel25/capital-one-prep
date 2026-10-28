An inventory service must accept reservations without selling stock that is not available.

Implement `reserve_stock(stock, requests)`. `stock` maps SKU names to available quantities. Each request has `sku` and `quantity`. Process requests in input order. Accept a request only when its SKU exists and its quantity is no greater than the remaining stock. Subtract the quantity only on success. An unknown SKU is rejected and must not be inserted. Return `{"accepted": [...], "stock": {...}}` with one boolean per request and the final stock for every original SKU, including zero balances. Empty inputs are allowed. Do not modify the inputs. Calls are independent.

**Constraints:**

- 0–300 SKUs and 0–300 requests. All required fields are present.
- SKU names are nonempty ASCII strings of at most 80 characters.
- Stock quantities are integers from 0 to 1000000000; requested quantities are integers from 1 to 1000000000.
- Inputs satisfy the contract; no validation is required.
- Do not change the input objects. Each call starts with fresh state.
- Python 3.11. Standard library only.

Implement `reserve_stock`. **Run** checks the examples. **Submit** checks all 14 cases.
