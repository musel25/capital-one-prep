## Approach

The reference processes the input in one pass. Time is O(n), and result storage is O(n). The output judge checks results. It cannot prove the requested Python technique. This is an in-memory exercise; it does not provide storage or concurrency control.

## Review of the AI claim

The claim adds a rule. The contract requires a nonempty string, not visible text. For `{"records": [{"id": " ", "amount": 6}, {"id": "", "amount": 6}]}`, expect `{"valid": [{"id": " ", "amount": 6}], "rejected": [1]}`. This pair separates empty from space-only text. It also checks that a repair does not silently trim IDs.

## Provenance

This guided repair reuses the verified behavior contract and independent oracle from Engineering 50 problem 07. The starter, reading task, test plan, and AI review exercise form a new lesson.

## Python implementation

```python
from typing import TypedDict

class Entry(TypedDict):
    id: str
    amount: int

def validate(value: object) -> Entry | None:
    if not isinstance(value, dict):
        return None
    identifier = value.get('id')
    amount = value.get('amount')
    if not isinstance(identifier, str) or not identifier:
        return None
    if type(amount) is not int or amount < 0:
        return None
    return {'id': identifier, 'amount': amount}

def solve(data: dict) -> dict:
    valid: list[Entry] = []
    rejected: list[int] = []
    for index, value in enumerate(data['records']):
        entry = validate(value)
        if entry is None:
            rejected.append(index)
        else:
            valid.append(entry)
    return {'valid': valid, 'rejected': rejected}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
