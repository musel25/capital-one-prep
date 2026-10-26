## Approach

The reference processes the input in one pass. Time is O(n), and result storage is O(n). The output judge checks results. It cannot prove the requested Python technique. This is an in-memory exercise; it does not provide storage or concurrency control.

## Python implementation

```python
from dataclasses import dataclass, field

@dataclass
class Box:
    name: str
    items: list[str] = field(default_factory=list)

def solve(data: dict) -> list[dict]:
    boxes = [Box(name) for name in data['names']]
    for action in data['actions']:
        boxes[action['box']].items.append(action['item'])
    return [{'name': box.name, 'items': box.items} for box in boxes]

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
