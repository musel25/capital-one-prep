"""Exercise the rendered learner text and the real sample-test extraction."""
from pathlib import Path


def test_literal_python_output_and_context_remain_visible():
    from cojudge.presentation import statement_text

    original = 'Practice subclasses.\n\n## Your task\n\nReturn `"<brand> <model> with <wheels> wheels"`.'
    rendered = statement_text(original, assumptions=['Names are nonempty strings.'])
    assert rendered.startswith('Practice subclasses.')
    assert '`"<brand> <model> with <wheels> wheels"`' in rendered
    assert 'Names are nonempty strings.' in rendered


def test_named_test_details_include_the_assertion_and_parameter_values():
    from cojudge.presentation import test_case_details

    tests = '''import pytest
@pytest.mark.parametrize("wheels", [0, 2])
def test_vehicle(wheels):
    vehicle = Vehicle("Yamaha", "R3", wheels)
    assert vehicle.description() == f"Yamaha R3 with {wheels} wheels"
'''
    details = test_case_details(tests, ['test_vehicle[0]', 'test_vehicle[2]'])
    assert 'assert vehicle.description()' in details['test_vehicle[0]']['code']
    assert '[0, 2]' in details['test_vehicle[2]']['code']
    assert details['test_vehicle[2]']['title'] == 'test_vehicle[2]'


def test_unknown_test_is_not_given_a_misleading_description():
    from cojudge.presentation import test_case_details

    assert test_case_details('def test_present():\n    assert 1 == 1\n', ['test_missing']) == {}


def test_official_checks_after_the_examples_also_have_readable_code():
    import json
    from cojudge.authoring.support import ROOT
    from cojudge.data_formats import support as formats
    from cojudge.datetimes_path import support as dates

    for module in (formats, dates):
        spec = module.load_specs([1])[0]
        folder = ROOT / 'cojudge/problems' / module.problem_id(spec)
        test_ids = [json.loads(case['payload'])['test'] for case in json.loads((folder / 'official-tests.json').read_text())]
        details = module.present_problem(spec, test_ids)['testCaseDescriptions']
        assert test_ids[-1] in details
        assert 'assert ' in details[test_ids[-1]]['code'] or 'raises' in details[test_ids[-1]]['code']
