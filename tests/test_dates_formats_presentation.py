"""Check the course builders' learner-facing presentation boundary."""
import importlib
import json

import pytest


@pytest.mark.parametrize('course,number', [('datetimes_path', 3), ('data_formats', 4)])
def test_builder_exposes_python_examples_and_actual_sample_tests(course, number, tmp_path):
    support = importlib.import_module(f'cojudge.{course}.support')
    spec = support.load_specs([number])[0]
    result = support.build_problem(spec, tmp_path)
    folder = tmp_path / 'problems' / result['id']
    metadata = json.loads((folder / 'metadata.json').read_text())

    # Internal test selectors must remain runnable without becoming the examples.
    assert all(json.loads(case['payload'])['test'] for case in metadata['testCases'])
    assert all(example['output'] != 'passed' for example in metadata['examples'])
    assert all(not example['input'].startswith('{"test":') for example in metadata['examples'])
    details = metadata['testCaseDescriptions']
    for test_id in result['tests'][:3]:
        assert test_id in details
        assert 'assert ' in details[test_id]['code']
    assert metadata['courseHelp']['body']


@pytest.mark.parametrize('course', ['datetimes_path', 'data_formats'])
def test_every_problem_has_a_presentation_without_changing_executable_content(course):
    support = importlib.import_module(f'cojudge.{course}.support')
    for spec in support.load_specs():
        before = {key: spec[key] for key in ('reference', 'template', 'tests')}
        presented = support.present_problem(spec, [])
        assert presented['statement']
        assert 1 <= len(presented['examples']) <= 3
        assert presented['testCaseDescriptions'] == {}
        assert all(spec[key] == value for key, value in before.items())
