## Independently checked trace

| Request | Current outcome | Current remaining | Required outcome | Required remaining |
|---|---|---:|---|---:|
| a | approved | 1000 | approved | 1000 |
| b | approved | 500 | rejected | 1000 |
| c | approved | 0 | rejected | 1000 |
| d | rejected | 0 | approved | 0 |
| e | rejected | 0 | rejected | 0 |

Both final budgets are zero, so checking only final state misses the incorrect approvals. Request b is the first counterexample. The merchant/limit check uses AND when either violation should reject; the expiration check admits the excluded endpoint.

```python
def authorize(card, request):
    if not card["active"] or request["at"] >= card["expires_at"]:
        return "rejected"
    if request["merchant"] != card["merchant"] or request["amount"] > card["per_transaction"]:
        return "rejected"
    if request["amount"] > card["remaining"]:
        return "rejected"
    card["remaining"] -= request["amount"]
    return "approved"

def preview_batch(card, requests):
    simulated = dict(card)
    results = [authorize(simulated, request) for request in requests]
    return {"results": results, "remaining": simulated["remaining"]}
```

preview_batch returns {"results":["approved","rejected","rejected","approved","rejected"],"remaining":0}; the original remaining stays 3000. Empty requests return an empty results list and the unchanged budget. The shallow copy is sufficient here because the contract contains only scalar card fields. This does not generalize automatically to nested mutable state.

Manual boundary checks: inactive card rejects without mutation; amount=per_transaction may approve; amount=per_transaction+1 rejects even with sufficient budget; at=expires_at rejects. Test a matching merchant with an excessive amount as well as the nonmatching merchant in the table. Batch time O(n), additional result space O(n); single authorization O(1).

Business discussion has multiple defensible answers. A possible success metric is completed legitimate purchases; a harm metric is false declines. Explain merchant matching, lifecycle and support costs as design questions, not facts about the company's systems. A limited rollout with monitoring is a possible next step.
