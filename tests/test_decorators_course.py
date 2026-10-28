"""Exercise the real Python 3.11 runner and the generated learner content."""
import json
import subprocess

import pytest

from cojudge.decorators_path.support import (
    COURSE_ID, build_problem, course_info, load_specs, problem_id, verify,
)


def test_course_keeps_all_twelve_exercises_in_learning_path_order():
    specs = load_specs()
    assert [spec['number'] for spec in specs] == list(range(1, 13))
    info = course_info(specs)
    ids = [pid for category in info['category-order'] for pid in info['problems-of-category'][category]]
    assert ids == [problem_id(spec) for spec in specs]
    assert len(set(ids)) == 12
    assert COURSE_ID == 'pybites-decorators-context-managers'


@pytest.mark.parametrize('number', range(1, 13))
def test_reference_passes_starter_fails_and_faults_are_rejected(number):
    result = verify(load_specs([number])[0])
    assert result['cases'] >= 5
    assert result['template_failures'] > 0
    assert len(result['mutations']) >= 3
    assert all(fault['detected_by'] for fault in result['mutations'])


def test_builder_exposes_actual_test_code_and_clean_python_template(tmp_path):
    spec = load_specs([2])[0]
    record = build_problem(spec, tmp_path)
    folder = tmp_path / 'problems' / record['id']
    assert {p.name for p in folder.iterdir()} == {
        'Marker.java', 'metadata.json', 'official-tests.json', 'statement.md', 'solution.md'}
    meta = json.loads((folder / 'metadata.json').read_text())
    assert list(meta['starterCode']) == ['python']
    assert meta['functionName'] == 'run'
    assert meta['testCaseDescriptions'][record['tests'][0]]['code'] in spec['tests']
    assert len(meta['testCases']) == 3
    assert len(json.loads((folder / 'official-tests.json').read_text())) == record['cases']
    assert 'recreated' in meta['courseHelp']['body'].lower()
    assert spec['reference'].strip() not in meta['starterCode']['python']
    assert 'payload' not in (folder / 'statement.md').read_text()


def test_verifier_rejects_an_equivalent_fault():
    spec = load_specs([1])[0]
    spec['mutations'] = [{'name': 'equivalent', 'old': '\n', 'new': '\n\n'}]
    with pytest.raises(AssertionError, match='survived'):
        verify(spec)


def test_references_pass_the_same_checks_under_real_pytest(tmp_path):
    for spec in load_specs():
        folder = tmp_path / f"bite_{spec['number']:02d}"
        folder.mkdir()
        (folder / f"{spec['module']}.py").write_text(spec['reference'])
        (folder / f"test_decorators_{spec['number']:02d}.py").write_text(spec['tests'])
    result = subprocess.run(['uv', 'run', 'pytest', '-q', str(tmp_path)],
                            capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
