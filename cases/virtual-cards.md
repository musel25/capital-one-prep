# Case: virtual-card authorization

Original constructed practice. No code execution during the attempt.

## Product discussion

A bank is considering merchant-locked virtual cards with expiration and spending controls. Who benefits, what can go wrong for legitimate customers, and how would you decide whether to roll out? Propose one success metric, one harm metric and a next step. Do not invent measured results.

## Rules and examples

This is a fictional merchant-locked virtual-card policy, not a description of Capital One's actual implementation.

All requests have positive integer-cent amounts and integer timestamps. The card must be active, the request timestamp must be strictly before expires_at, the merchant must match, the amount must not exceed per_transaction, and enough remaining budget must exist. All five conditions are required. Only approved requests reduce remaining; rejected requests change nothing. Process the supplied requests in table order, even when timestamps are not sorted.

Initial card: active=True, merchant="M1", expires_at=100, per_transaction=2000, remaining=3000.

| id | at | merchant | amount |
|---|---:|---|---:|
| a | 99 | M1 | 2000 |
| b | 99 | M2 | 500 |
| c | 100 | M1 | 500 |
| d | 99 | M1 | 1000 |
| e | 99 | M1 | 1 |

Predict each required outcome and remaining budget before reading the implementation.

## Read the implementation

Trace actual outcomes and remaining budget after each request. Identify the first mismatch with the required behavior.

```python
def authorize(card, request):
    if not card["active"] or request["at"] > card["expires_at"]:
        return "rejected"
    if request["merchant"] != card["merchant"] and request["amount"] > card["per_transaction"]:
        return "rejected"
    if request["amount"] > card["remaining"]:
        return "rejected"
    card["remaining"] -= request["amount"]
    return "approved"
```

## Correct and extend

Correct authorize without changing the contract. Then implement preview_batch(card, requests), returning {results: [status per request], remaining: simulated final budget} while preserving the original card and requests. Use the same rules and supplied order. Predict the sample and an empty batch. Explain why matching final balances alone does not prove correctness.
