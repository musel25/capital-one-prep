## Approach

Validate each body without changing it. Accumulate field names in contract order, then build one response. Time is linear in the number of input fields and characters. Output space is linear in the number of bodies. Real APIs also limit byte size and nesting before decoding.

## Review of the AI claim

The claim is incorrect. The contract distinguishes JSON integer tokens from decimal or exponent notation. For bodies `[{"account": "z", "amount": 1.0}, {"account": "z", "amount": 1}]`, expect `[ {"status": 422, "errors": ["amount"]}, {"status": 201, "body": {"account": "z", "amount": 1, "note": null}} ]`. Equal mathematical value does not establish the required runtime type.

## Provenance

This guided repair reuses the verified behavior contract and independent oracle from Engineering 50 problem 22. The starter, reading task, test plan, and AI review exercise form a new lesson.

## Python implementation

```python
import re

def solve(data):
    out = []
    for body in data["bodies"]:
        if not isinstance(body, dict):
            out.append({"status": 400, "errors": ["body"]})
            continue
        errors = []
        account = body.get("account")
        amount = body.get("amount")
        note = body.get("note")
        if not isinstance(account, str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,11}", account):
            errors.append("account")
        if type(amount) is not int or not 1 <= amount <= 10000:
            errors.append("amount")
        if note is not None and (not isinstance(note, str) or len(note) > 20):
            errors.append("note")
        if set(body) - {"account", "amount", "note"}:
            errors.append("unknown")
        if errors:
            out.append({"status": 422, "errors": errors})
        else:
            out.append({"status": 201, "body": {"account": account, "amount": amount, "note": note}})
    return out

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
