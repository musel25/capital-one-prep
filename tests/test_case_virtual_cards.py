"""Check the constructed case's traces independently of its explanatory prose."""
import copy
import json
import re
from pathlib import Path


def test_virtual_card_actual_and_corrected_sequences_and_nonmutating_preview():
    root = Path(__file__).resolve().parents[1]
    plan = json.loads((root / 'curriculum/plan.json').read_text())
    case = next(b for d in plan['days'] for b in d['blocks'] if b['id'] == 'd06-case-v2')
    source = next(s['content'] for s in case['stages'] if '```python' in s['content'])
    current, corrected = {}, {}
    exec(re.search(r'```python\n(.*?)```', source, re.S)[1], current)
    exec(re.search(r'```python\n(.*?)```', case['solution'], re.S)[1], corrected)
    card = dict(active=True, merchant='M1', expires_at=100, per_transaction=2000, remaining=3000)
    rows = [dict(at=t, merchant=m, amount=a) for t, m, a in
            [(99, 'M1', 2000), (99, 'M2', 500), (100, 'M1', 500), (99, 'M1', 1000), (99, 'M1', 1)]]
    actual_card, fixed_card = dict(card), dict(card)
    def trace(function, state):
        results = []
        for row in rows:
            results.append((function(state, row), state['remaining']))
        return results
    assert trace(current['authorize'], actual_card) == [('approved', 1000), ('approved', 500), ('approved', 0), ('rejected', 0), ('rejected', 0)]
    assert trace(corrected['authorize'], fixed_card) == [('approved', 1000), ('rejected', 1000), ('rejected', 1000), ('approved', 0), ('rejected', 0)]
    before = copy.deepcopy((card, rows))
    assert corrected['preview_batch'](card, rows) == {'results': ['approved', 'rejected', 'rejected', 'approved', 'rejected'], 'remaining': 0}
    assert (card, rows) == before
    assert corrected['preview_batch'](card, []) == {'results': [], 'remaining': 3000}
    for request in [dict(at=99, merchant='M1', amount=2001), dict(at=100, merchant='M1', amount=1)]:
        assert corrected['authorize'](card, request) == 'rejected'
        assert card['remaining'] == 3000
