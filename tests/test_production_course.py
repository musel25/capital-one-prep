"""Test real course references, faulty variants, adapters, and Java markers."""
import copy
import json

import pytest


def test_course_contracts_references_and_fault_checks(tmp_path):
    from cojudge.production.support import load_specs, verify, build_problem

    specs = load_specs()
    assert [s['number'] for s in specs] == list(range(1, 25))
    for spec in specs:
        report = verify(spec)
        assert report['cases'] >= 12
        assert len(report['mutations']) >= 3
        record = build_problem(spec, tmp_path)
        folder = tmp_path / 'problems' / record['id']
        metadata = json.loads((folder / 'metadata.json').read_text())
        namespace = {'__name__': 'learner'}
        exec(metadata['starterCode']['python'], namespace)
        with pytest.raises(NotImplementedError):
            namespace['Solution']().run(json.dumps(spec['cases'][0]['input']))


def test_equivalent_mutation_does_not_count_as_a_detected_fault():
    from cojudge.production.support import load_specs, verify

    spec = copy.deepcopy(load_specs()[0])
    spec['mutations'] = [{'name': 'equivalent', 'old': 'return out', 'new': 'return list(out)'}]
    with pytest.raises(AssertionError, match='survived'):
        verify(spec)


def test_independent_java_markers_match_all_manual_expectations(tmp_path):
    from cojudge.production.support import load_specs, verification_spec
    from cojudge.authoring.support import check_java

    for spec in load_specs():
        report = check_java(verification_spec(spec), tmp_path)
        assert report['cases'] == len(spec['cases'])
        assert report['wrong_rejected'] >= len(spec['cases'])


def test_judge_adapter_rejects_input_changes_even_with_correct_output():
    from cojudge.production.support import full_source, load_specs

    spec = load_specs([1])[0]
    source = 'def clean_emails(emails):\n    emails.clear()\n    return ["a@b"]\n'
    namespace = {}
    exec(full_source(spec, source), namespace)
    with pytest.raises(ValueError, match='input'):
        namespace['Solution']().run('{"emails":["a@b"]}')


def test_live_check_counts_user_runtime_errors_but_rejects_infrastructure_errors():
    from scripts.production_course import rejection_kind

    actual_runtime_failure = {
        'ready': True,
        'error': 'Submission failed: details: Traceback (most recent call last):\n  File "/app/Solution.py", line 5, in paginate_records\nIndexError: list index out of range',
        'errorTestCase': {'payload': '{"records":[{"id":1}],"limit":1,"after_id":0}'},
        'errorTestIndex': 4,
    }
    assert rejection_kind(actual_runtime_failure) == 'runtime_error'
    assert rejection_kind({'accepted': False, 'results': [{'isCorrect': False}]}) == 'wrong_answer'
    with pytest.raises(AssertionError):
        rejection_kind({'ready': True, 'error': 'Docker is unavailable'})
    with pytest.raises(AssertionError):
        rejection_kind({'accepted': True, 'results': [{'isCorrect': True}]})
