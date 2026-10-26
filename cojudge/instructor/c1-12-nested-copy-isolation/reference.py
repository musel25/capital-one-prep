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
