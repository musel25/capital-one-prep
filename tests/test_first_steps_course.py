"""Python First Steps: two independent implementations agree; starters and faults fail."""
import json

import pytest

from cojudge.authoring.support import ROOT
from cojudge.first_steps.support import COURSE_ID, course_info, numbered, problem_id, verify

CASES = numbered()


@pytest.mark.parametrize('number,spec', CASES, ids=[problem_id(n, s) for n, s in CASES])
def test_exercise_verifies(number, spec):
    result = verify(number, spec)
    assert result['starter_failures'] > 0


def test_course_lists_all_25_exercises_in_order():
    info = course_info()
    listed = [pid for category in info['category-order'] for pid in info['problems-of-category'][category]]
    assert listed == [problem_id(n, s) for n, s in CASES]
    assert len(listed) == 25


def test_generated_content_is_current():
    saved = json.loads((ROOT / 'cojudge/courses' / COURSE_ID / 'courseinfo.json').read_text())
    assert saved == course_info()
    for number, spec in CASES:
        meta = json.loads((ROOT / 'cojudge/problems' / problem_id(number, spec) / 'metadata.json').read_text())
        assert meta['scriptMode'] is True
        assert meta['starterCode'] == {'python': spec['starter']}
