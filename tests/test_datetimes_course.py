"""Validate the new path without changing existing courses or learner work."""
import pytest
from cojudge.datetimes_path.support import load_specs, course_info, problem_id, verify


def test_complete_path_and_order():
    specs = load_specs()
    assert [s['number'] for s in specs] == list(range(1, 25))
    assert len({problem_id(s) for s in specs}) == 24
    info = course_info(specs)
    ids = [pid for group in info['problems-of-category'].values() for pid in group]
    assert ids == [problem_id(s) for s in specs]
    assert specs[0]['title'] == 'Pybites date generator'
    assert specs[-1]['title'] == "Calculate my mac's longest uptime"


def test_sources_contracts_and_fault_checks():
    for spec in load_specs():
        assert spec['contract'] and spec['mutations']
        assert spec['page']['desc_html']
        if spec.get('original'):
            assert spec['template'] == spec['page']['template']
            assert spec['page']['tests'] in spec['tests']
    assert [s['number'] for s in load_specs() if s.get('original')] == [1, 2]


def test_verification_checks_every_reference_starter_and_fault():
    for spec in load_specs():
        result = verify(spec)
        assert result['cases'] >= 5
        assert result['template_failures'] > 0
        assert all(m['detected_by'] for m in result['mutations'])


def test_verifier_rejects_a_surviving_mutation():
    spec = load_specs([1])[0]
    spec['mutations'] = [{'name': 'equivalent', 'old': 'days=100', 'new': 'days=10 * 10'}]
    with pytest.raises(AssertionError, match='survived'):
        verify(spec)
