"""Execute the published fictional rules and verify independently derived traces."""
import json
import re
from pathlib import Path


def test_published_card_number_trace_and_correction():
    plan = json.loads((Path(__file__).resolve().parents[1] / 'curriculum/plan.json').read_text())
    cases = [b for d in plan['days'] for b in d['blocks'] if b['id'] == 'd06-case-v3']
    assert len(cases) == 1, 'Schedule the new card-number case separately from authorization.'
    case = cases[0]
    current, corrected = {}, {}
    code_stage = next(s for s in case['stages'] if '```python' in s['content'])
    exec(re.search(r'```python\n(.*?)```', code_stage['content'], re.S)[1], current)
    exec(re.search(r'```python\n(.*?)```', case['solution'], re.S)[1], corrected)
    numbers = ['04123459', '07123452', '04123450', '04112222', '04000004',
               '09123454', '0412345', '04123A59', '０4123459', '04333003']
    assert [current['is_valid'](s) for s in numbers] == [
        True, True, True, True, False, False, False, False, False, True]
    expected = [True, True, False, False, False, False, False, False, False, True]
    assert [corrected['is_valid'](s) for s in numbers] == expected
    original = list(numbers)
    assert corrected['classify'](numbers) == expected
    assert numbers == original
    assert corrected['classify']([]) == []
    assert corrected['classify'](['04123459'] * 2) == [True, True]
    for invalid in ['', ' 04123459', '04123459 ', '041234590', '041234５9']:
        assert corrected['is_valid'](invalid) is False
