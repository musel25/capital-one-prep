"""Validate displayed ticket calls against their independent expected results."""
from cojudge.production import support


def test_ticket_example_calls_use_the_real_arguments_and_expected_results():
    for spec in support.load_specs():
        namespace = {}
        exec(spec['reference'], namespace)
        presentation = support.present_problem(spec, [])
        for example, case in zip(presentation['examples'], spec['cases'][:3], strict=True):
            assert eval(example['input'], namespace) == case['expected']
            assert example['output'] == repr(case['expected'])
