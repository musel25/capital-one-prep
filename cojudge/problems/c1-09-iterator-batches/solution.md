## Approach

The reference consumes one iterator with islice. Time is O(n). The active batch uses O(size) space, but this JSON return value stores O(n) items. The judge cannot prove iterator use or memory complexity. Production consumers can process each batch as it is produced.

## Python implementation

```python
from itertools import islice

def solve(data: dict) -> list[list[int]]:
    values = iter(data['values'])
    batches = []
    while True:
        batch = list(islice(values, data['size']))
        if not batch:
            break
        batches.append(batch)
    return batches

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
