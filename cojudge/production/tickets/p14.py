"""Reserve inventory in request order."""


def case(stock, requests, accepted, remaining, label):
    return {"input": {"stock": stock, "requests": requests},
            "expected": {"accepted": accepted, "stock": remaining}, "label": label}


CASES = [
    case({}, [], [], {}, "empty inventory and request list"),
    case({"a": 5}, [], [], {"a": 5}, "no requests preserve stock"),
    case({"a": 5}, [{"sku": "a", "quantity": 2}], [True], {"a": 3}, "successful reservation"),
    case({"a": 5}, [{"sku": "a", "quantity": 5}], [True], {"a": 0}, "exact stock is accepted"),
    case({"a": 5}, [{"sku": "a", "quantity": 6}], [False], {"a": 5}, "insufficient stock is unchanged"),
    case({"a": 0}, [{"sku": "a", "quantity": 1}], [False], {"a": 0}, "zero stock rejects a request"),
    case({}, [{"sku": "missing", "quantity": 1}], [False], {}, "unknown SKU is not inserted"),
    case({"a": 2}, [{"sku": "b", "quantity": 1}, {"sku": "a", "quantity": 1}],
         [False, True], {"a": 1}, "unknown request does not block later requests"),
    case({"a": 5}, [{"sku": "a", "quantity": 3}, {"sku": "a", "quantity": 3}],
         [True, False], {"a": 2}, "requests consume remaining stock"),
    case({"a": 2}, [{"sku": "a", "quantity": 3}, {"sku": "a", "quantity": 2}],
         [False, True], {"a": 0}, "failed reservation does not consume stock"),
    case({"a": 4}, [{"sku": "a", "quantity": 2}, {"sku": "a", "quantity": 2},
                    {"sku": "a", "quantity": 1}],
         [True, True, False], {"a": 0}, "repeated reservations are separate requests"),
    case({"a": 2, "b": 3, "unused": 0},
         [{"sku": "b", "quantity": 2}, {"sku": "a", "quantity": 2}, {"sku": "b", "quantity": 2}],
         [True, True, False], {"a": 0, "b": 1, "unused": 0}, "SKUs have separate inventory"),
    case({"A": 2, "a": 3}, [{"sku": "A", "quantity": 1}, {"sku": "a", "quantity": 3}],
         [True, True], {"A": 1, "a": 0}, "SKU names are case sensitive"),
    case({"bulk": 1000000000}, [{"sku": "bulk", "quantity": 999999999},
                               {"sku": "bulk", "quantity": 1}],
         [True, True], {"bulk": 0}, "large stock reaches zero exactly"),
]

CASES = CASES[2:5] + CASES[:2] + CASES[5:]

SPEC = {
    "number": 14,
    "slug": "reserve-stock",
    "title": "Reserve stock in request order",
    "difficulty": "Medium",
    "category": "03-stateful-services",
    "ticket": "An inventory service must accept reservations without selling stock that is not available.",
    "task": "Implement `reserve_stock(stock, requests)`. `stock` maps SKU names to available quantities. "
            "Each request has `sku` and `quantity`. Process requests in input order. Accept a request "
            "only when its SKU exists and its quantity is no greater than the remaining stock. "
            "Subtract the quantity only on success. An unknown SKU is rejected and must not be "
            "inserted. Return `{\"accepted\": [...], \"stock\": {...}}` with one boolean per request "
            "and the final stock for every original SKU, including zero balances. Empty inputs "
            "are allowed. Do not modify the inputs. Calls are independent.",
    "constraints": ["0–300 SKUs and 0–300 requests. All required fields are present.",
                    "SKU names are nonempty ASCII strings of at most 80 characters.",
                    "Stock quantities are integers from 0 to 1000000000; requested quantities are integers from 1 to 1000000000.",
                    "Inputs satisfy the contract; no validation is required."],
    "function": "reserve_stock",
    "starter": "def reserve_stock(stock, requests):\n    raise NotImplementedError\n",
    "reference": '''def reserve_stock(stock, requests):
    remaining = dict(stock)
    accepted = []
    for request in requests:
        sku, quantity = request["sku"], request["quantity"]
        enough = sku in remaining and remaining[sku] >= quantity
        if enough:
            remaining[sku] -= quantity
        accepted.append(enough)
    return {"accepted": accepted, "stock": remaining}
''',
    "java": '''public Object solve(Map<String,Object> d) {
    Map<String,Object> remaining = new LinkedHashMap<>(obj(d.get("stock")));
    List<Object> accepted = new ArrayList<>();
    for (Object raw : arr(d.get("requests"))) {
        Map<String,Object> request = obj(raw);
        String sku = s(request.get("sku"));
        long quantity = lng(request.get("quantity"));
        boolean ok = remaining.containsKey(sku) && lng(remaining.get(sku)) >= quantity;
        accepted.add(ok);
        if (ok) remaining.put(sku, lng(remaining.get(sku)) - quantity);
    }
    return map("accepted", accepted, "stock", remaining);
}''',
    "cases": CASES,
    "mutations": [
        {"name": "rejects_exact_stock", "old": 'remaining[sku] >= quantity',
         "new": 'remaining[sku] > quantity'},
        {"name": "successful_request_does_not_consume_stock", "old": 'remaining[sku] -= quantity',
         "new": 'remaining[sku] -= 0'},
        {"name": "unknown_sku_is_inserted", "old": 'accepted.append(enough)',
         "new": 'remaining.setdefault(sku, 0)\n        accepted.append(enough)'},
    ],
}
