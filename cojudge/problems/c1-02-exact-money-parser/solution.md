## Approach

The reference processes the input in one pass. Time is O(n), and result storage is O(n). The output judge checks results. It cannot prove the requested Python technique. This is an in-memory exercise; it does not provide storage or concurrency control.

## Python implementation

```python
import re
from decimal import Decimal

def solve(data: dict) -> dict:
    cents = []
    for value in data['amounts']:
        if isinstance(value, str) and re.fullmatch(r'-?[0-9]{1,12}(?:\.[0-9]{1,2})?', value):
            cents.append(int(Decimal(value) * 100))
        else:
            cents.append(None)
    return {'cents': cents}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
