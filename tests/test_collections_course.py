"""Verify the complete course and its actual Python 3.11 judge runner."""
import json

import pytest

from cojudge.collections_path.support import build_problem, course_info, load_specs, verify


def test_course_contains_all_eleven_bites_in_source_order():
    specs = load_specs()
    assert [s['number'] for s in specs] == list(range(1, 12))
    info = course_info(specs)
    ids = [pid for group in info['problems-of-category'].values() for pid in group]
    assert len(ids) == len(set(ids)) == 11
    assert [int(pid.split('-')[1]) for pid in ids] == list(range(1, 12))
    for spec in specs:
        assert spec['contract'] and spec['mutations']
        assert 'BLOCKED' not in spec['page']['desc_html']
        assert '\r' not in spec['page']['desc_html']


@pytest.mark.parametrize('number', range(1, 12))
def test_reference_passes_starter_fails_and_real_faults_are_detected(number):
    result = verify(load_specs([number])[0])
    assert result['cases'] >= 5
    assert result['template_failures'] > 0
    assert all(fault['detected_by'] for fault in result['mutations'])


def test_builder_writes_a_complete_python_only_problem(tmp_path):
    spec = load_specs([2])[0]
    record = build_problem(spec, tmp_path)
    folder = tmp_path / 'problems' / record['id']
    assert {p.name for p in folder.iterdir()} == {
        'Marker.java', 'metadata.json', 'official-tests.json', 'statement.md', 'solution.md'}
    metadata = json.loads((folder / 'metadata.json').read_text())
    assert list(metadata['starterCode']) == ['python']
    assert metadata['functionName'] == 'run'
    assert len(metadata['testCases']) == 3
    assert len(json.loads((folder / 'official-tests.json').read_text())) == record['cases']
    assert 'pybites-collections' in (folder / 'statement.md').read_text()


def test_equivalent_mutation_is_rejected_by_verifier():
    spec = load_specs([1])[0]
    spec['mutations'] = [{'name': 'equivalent', 'old': 'sum(', 'new': 'sum( '}]
    with pytest.raises(AssertionError, match='survived'):
        verify(spec)
