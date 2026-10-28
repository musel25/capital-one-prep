"""Check that learner examples and check cards describe the actual exercise."""
import ast
import importlib

import pytest


@pytest.mark.parametrize('course', ['fastapi', 'sqlmodel', 'typer', 'pytest'])
def test_presentations_use_actual_examples_and_source_code(course):
    support = importlib.import_module(f'cojudge.{course}_path.support')
    for spec in support.load_specs():
        if course == 'pytest':
            ids = support.checks(spec)
        elif course == 'sqlmodel':
            ids = support.test_ids(spec)
        elif course == 'typer':
            ids = [node.name for node in ast.parse(spec['tests']).body
                   if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')]
        else:
            ids = spec['test_ids']
        result = support.present_problem(spec, ids)
        assert result['statement'].strip()
        assert not result['statement'].startswith('# ')
        assert result['examples']
        assert all(example['output'] != 'passed' for example in result['examples'])
        assert set(result['testCaseDescriptions']) == set(ids)
        assert all(card['title'] and card['code'] for card in result['testCaseDescriptions'].values())
        assert result['courseHelp']['body']
        if course == 'pytest':
            assert result['testCaseDescriptions']['baseline']['code'] == spec['target'].strip()
        else:
            assert all(card['code'] in spec['tests'] for card in result['testCaseDescriptions'].values())
