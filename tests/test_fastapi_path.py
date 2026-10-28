"""Check the FastAPI course with the same adapter used by Cojudge."""
import pytest

from cojudge.fastapi_path.support import load_specs, run_all, verify


def test_path_contains_all_ten_exercises_in_source_order():
    specs = load_specs()
    assert [spec['number'] for spec in specs] == list(range(1, 11))
    assert all(spec['tests'] and spec['contract'] and spec['mutations'] for spec in specs)


def test_runner_executes_real_fastapi_requests_and_rejects_wrong_responses():
    spec = load_specs([1])[0]
    assert all(value == 'passed' for value in run_all(spec, spec['reference']).values())
    wrong = spec['reference'].replace("Welcome to PyBites' FastAPI Learning Path 🐍 🎉", 'wrong')
    assert any(value != 'passed' for value in run_all(spec, wrong).values())


def test_verifier_rejects_an_undetected_fault():
    spec = load_specs([1])[0]
    spec['mutations'] = [('equivalent', 'return {', 'return  {')]
    with pytest.raises(AssertionError, match='survived'):
        verify(spec)
