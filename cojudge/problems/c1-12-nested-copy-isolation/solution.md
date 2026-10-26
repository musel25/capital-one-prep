## Approach

The reference uses deepcopy once per requested configuration. If the template has t values and there are n changes, time and result space are O(n t). Tests expose shared nested lists and dictionaries through the returned template and copies. The judge cannot prove copy strategy. Deep copying arbitrary application objects can need a different policy.

## Python implementation

```python
from copy import deepcopy

def solve(data: dict) -> dict:
    template = data['template']
    copies = []
    for change in data['changes']:
        config = deepcopy(template)
        for key in ('daily', 'monthly'):
            if key in change:
                config['limits'][key] = change[key]
        if 'tag' in change:
            config['tags'].append(change['tag'])
        copies.append(config)
    return {'template': template, 'copies': copies}

# Supplied CoJudge adapter. Implement solve(data) above.
import json

class Solution:
    def run(self, payload: str) -> str:
        return json.dumps(solve(json.loads(payload)), ensure_ascii=True, allow_nan=False)

```
