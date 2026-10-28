"""Check course completeness and the real Python 3.11 judge contract."""
import importlib
import json
from pathlib import Path

import pytest


def support():
    path = Path(__file__).resolve().parents[1] / 'cojudge/data_formats/support.py'
    assert path.exists(), 'Data Formats course builder is missing'
    return importlib.import_module('cojudge.data_formats.support')


def test_all_seventeen_exercises_keep_the_source_order():
    course = support()
    specs = course.load_specs()
    assert [s['number'] for s in specs] == list(range(1, 18))
    info = course.course_info(specs)
    ids = [pid for cat in info['category-order'] for pid in info['problems-of-category'][cat]]
    assert ids == [course.problem_id(s) for s in specs]
    assert len(set(ids)) == 17
    for spec in specs:
        assert spec['contract'] and spec['mutations']
        assert 'BLOCKED' not in spec['page']['desc_html']


@pytest.mark.parametrize('number', range(1, 18))
def test_references_pass_starters_fail_and_faults_are_detected(number):
    result = support().verify(support().load_specs([number])[0])
    assert result['cases'] >= 5
    assert result['template_failures'] > 0
    assert all(fault['detected_by'] for fault in result['mutations'])


def test_builder_writes_complete_problem_and_original_link(tmp_path):
    course = support()
    spec = course.load_specs([4])[0]
    result = course.build_problem(spec, tmp_path)
    folder = tmp_path / 'problems' / result['id']
    assert {p.name for p in folder.iterdir()} == {
        'Marker.java', 'metadata.json', 'official-tests.json', 'statement.md', 'solution.md'}
    meta = json.loads((folder / 'metadata.json').read_text())
    assert list(meta['starterCode']) == ['python']
    assert meta['link'].startswith('https://pybitesplatform.com/bites/')
    assert len(meta['testCases']) == 3
    assert len(json.loads((folder / 'official-tests.json').read_text())) == result['cases']
    assert 'pybites-data-formats' in (folder / 'statement.md').read_text()


def test_available_free_tests_are_preserved_before_added_cases():
    for spec in support().load_specs([4, 6]):
        assert spec['tests'].startswith(spec['page']['tests'])


def test_verifier_rejects_a_fault_that_is_not_detected():
    course = support()
    spec = course.load_specs([4])[0]
    spec['mutations'] = [{'name': 'equivalent', 'old': 'json.dumps(', 'new': 'json.dumps( '}]
    with pytest.raises(AssertionError, match='survived'):
        course.verify(spec)


def test_live_starter_check_requires_a_real_judge_rejection():
    from scripts import data_formats_course
    check = getattr(data_formats_course, 'assert_rejected', None)
    assert check is not None, 'Live checks must distinguish failed tests from infrastructure errors'
    check({'ready': True, 'accepted': False, 'results': [{'isCorrect': False}]})
    with pytest.raises(AssertionError):
        check({'ready': True, 'error': 'Docker unavailable'})
    with pytest.raises(AssertionError):
        check({'ready': True, 'accepted': True, 'results': [{'isCorrect': True}]})
