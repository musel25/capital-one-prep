## Approach

The reference uses csv.reader, then one dictionary for totals. Time is O(c), where c is the text length. Space is O(c + k) for the input stream and k accounts. Tests cover quoted commas, quotes, and embedded line breaks. The output judge cannot certify use of csv. This exercise assumes valid CSV and does not define malformed-file recovery.

## Python implementation

```python
import csv
from io import StringIO

def solve(data: dict) -> list[dict]:
    records = csv.reader(StringIO(data['csv'], newline=''))
    next(records)
    totals = {}
    for account, amount in records:
        totals[account] = totals.get(account, 0) + int(amount)
    return [{'account': account, 'total': total} for account, total in totals.items()]

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
