"""Exercise the test-writing judge with weak, invalid, and complete suites."""
import importlib.util
from pathlib import Path


def support():
    path = Path('cojudge/pytest_path/support.py')
    assert path.exists(), 'The Pytest path judge is not implemented'
    spec = importlib.util.spec_from_file_location('pytest_path_support', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_empty_suite_cannot_pass():
    api = support()
    spec = api.load_specs()[0]
    results = api.run_all(spec, 'from fibonacci import fib\n')
    assert results['baseline'].startswith('FAILED')
    assert all(value != 'passed' for value in results.values())


def test_false_assertions_cannot_kill_mutants():
    api = support()
    spec = api.load_specs()[0]
    results = api.run_all(spec, 'def test_wrong():\n    assert False\n')
    assert all(value != 'passed' for value in results.values())


def test_weak_suite_leaves_mutants_alive():
    api = support()
    spec = api.load_specs()[0]
    results = api.run_all(spec, 'from fibonacci import fib\ndef test_one():\n    assert fib(1) == 1\n')
    assert any('SURVIVED' in value for value in results.values())


def test_reference_suites_pass_and_each_starter_fails():
    api = support()
    specs = api.load_specs()
    assert len(specs) == 10
    for spec in specs:
        assert set(api.run_all(spec, spec['reference']).values()) == {'passed'}, spec['title']
        assert 'FAILED' in api.run_all(spec, spec['starter'])['baseline'], spec['title']


def test_fixture_can_return_a_generator_without_being_a_yield_fixture():
    api = support()
    spec = api.load_specs()[5]
    results = api.run_all(spec, spec['reference'])
    assert results['baseline'] == 'passed'


def test_capture_includes_stderr_and_readouterr_resets_both_streams():
    api = support()
    spec = api.load_specs()[2]
    suite = '''
import sys
from printing import print_even_numbers

def test_streams(capsys):
    print_even_numbers([0, 1, 2])
    print('problem', file=sys.stderr)
    captured = capsys.readouterr()
    assert captured.out == '0\\n2\\n'
    assert captured.err == 'problem\\n'
    assert capsys.readouterr().out == ''
    assert capsys.readouterr().err == ''
'''
    assert api.run_all(spec, suite)['baseline'] == 'passed'


def test_fixture_dependency_is_cached_and_teardown_runs_before_next_test():
    api = support()
    spec = api.load_specs()[3]
    suite = '''
import pytest
from fizzbuzz import fizzbuzz
state = []

@pytest.fixture
def resource():
    value = []
    state.append('open')
    yield value
    state.append('closed')

@pytest.fixture
def dependent(resource):
    return resource

def test_first(resource, dependent):
    assert resource is dependent
    assert state == ['open']
    assert fizzbuzz(15) == 'FizzBuzz'
    assert fizzbuzz(3) == 'Fizz'
    assert fizzbuzz(5) == 'Buzz'
    assert fizzbuzz(1) == 1

def test_second():
    assert state == ['open', 'closed']
'''
    assert api.run_all(spec, suite)['baseline'] == 'passed'


def test_patch_decorator_injects_mocks_before_real_fixtures():
    api = support()
    spec = api.load_specs()[5]
    suite = '''
from unittest.mock import patch
from colors import gen_hex_color

@patch('colors.sample', return_value=list('A1B2C3'))
def test_mocked(mock_sample, tmp_path):
    assert next(gen_hex_color()) == '#A1B2C3'
    mock_sample.assert_called_once_with('0123456789ABCDEF', 6)
    assert tmp_path.is_dir()
'''
    assert api.run_all(spec, suite)['baseline'] == 'passed'


def test_builtin_tmp_path_is_shared_with_fixture_dependencies():
    api = support()
    spec = api.load_specs()[3]
    suite = '''
import pytest
from fizzbuzz import fizzbuzz

@pytest.fixture
def file_path(tmp_path):
    return tmp_path / 'data.txt'

def test_file(file_path, tmp_path):
    assert file_path.parent == tmp_path
    assert fizzbuzz(15) == 'FizzBuzz'
    assert fizzbuzz(3) == 'Fizz'
    assert fizzbuzz(5) == 'Buzz'
    assert fizzbuzz(1) == 1
'''
    assert api.run_all(spec, suite)['baseline'] == 'passed'
