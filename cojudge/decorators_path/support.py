"""Build native Cojudge content with the existing Python 3.11 Pybites runner."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from cojudge.authoring.support import ROOT, write_json
from cojudge.presentation import course_help, test_case_details
from cojudge.pybites.runner import MARKER
from cojudge.pybites.support import full_source, run_all

COURSE_ID = 'pybites-decorators-context-managers'
HERE = Path(__file__).parent
LEVELS = {'Beginner': ('01-beginner', 'Easy'),
          'Intermediate': ('02-intermediate', 'Medium'),
          'Advanced': ('03-advanced', 'Hard')}


def load_specs(numbers=None):
    pages = json.loads((HERE / 'source-pages.json').read_text())
    specs = []
    for page in pages:
        if numbers and page['n'] not in numbers:
            continue
        file = HERE / 'bites' / f"b{page['n']:02d}.py"
        module_spec = importlib.util.spec_from_file_location(f"decorators_b{page['n']:02d}", file)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        spec = {**module.SPEC, 'number': page['n'], 'page': page}
        for field in ('template', 'tests', 'reference'):
            spec[field] = spec[field].replace('\r\n', '\n')
        specs.append(spec)
    return specs


def problem_id(spec):
    return f"pbdc-{spec['number']:02d}-{spec['page']['slug']}"


def verify(spec):
    results = run_all(spec, spec['reference'])
    failed = {name: value for name, value in results.items() if value != 'passed'}
    assert results and not failed, f"{problem_id(spec)} reference failed: {failed}"
    starter = run_all(spec, spec['template'])
    assert any(value != 'passed' for value in starter.values()), f"{problem_id(spec)} starter passed all tests"
    mutations = []
    for fault in spec['mutations']:
        assert fault['old'] in spec['reference'], f"Missing fault target: {fault['name']}"
        code = spec['reference'].replace(fault['old'], fault['new'], fault.get('count', 1))
        compile(code, '<fault>', 'exec')
        faulty = run_all(spec, code)
        detected = [name for name, value in faulty.items() if value != 'passed']
        assert detected, f"Mutation survived: {fault['name']}"
        mutations.append({'name': fault['name'], 'detected_by': detected})
    return {'id': problem_id(spec), 'cases': len(results), 'tests': list(results),
            'template_failures': sum(value != 'passed' for value in starter.values()),
            'mutations': mutations}


def course_info(specs):
    return {
        'title': 'Pybites Decorators and Context Managers Path',
        'description': 'The 12 exercises from the Pybites Decorators and Context Managers learning path, '
                       'in their original order. Practice decorators, context managers, singledispatch, '
                       'caching, and retries. The Account exercise keeps its original free template '
                       'and tests. Other templates and tests are recreated from public descriptions. Select Python.',
        'category-order': [category for category, _ in LEVELS.values()],
        'problems-of-category': {
            category: [problem_id(spec) for spec in specs if spec['page']['level'] == level]
            for level, (category, _) in LEVELS.items()
        }
    }


def build_problem(spec, destination=ROOT / 'cojudge'):
    result = verify(spec)
    folder = Path(destination) / 'problems' / result['id']
    folder.mkdir(parents=True, exist_ok=True)
    category, difficulty = LEVELS[spec['page']['level']]
    payloads = [{'payload': json.dumps({'test': name})} for name in result['tests']]
    origin = ('The original free Account template and tests are retained, with added boundary tests.'
              if spec.get('original') else
              'This template and these tests are recreated from the public description. '
              'The local API and extra input guarantees are stated in the problem.')
    metadata = {
        'id': result['id'], 'title': f"{spec['number']:02d}. {spec['title']}",
        'difficulty': difficulty, 'link': '', 'category': category,
        'examples': spec['examples'],
        'testCaseDescriptions': test_case_details(spec['tests'], result['tests']),
        'courseHelp': course_help(spec['page']['url'],
                                  ' '.join(filter(None, [origin, spec.get('notes'),
                                                         'Use Python 3.11 and the standard library.']))),
        'starterCode': {'python': full_source(spec, spec['template'])},
        'testCases': payloads[:3], 'functionName': 'run',
        'params': [{'name': 'payload', 'type': 'string'}], 'outputType': 'string',
        'hints': spec.get('hints', [])
    }
    write_json(folder / 'metadata.json', metadata)
    write_json(folder / 'official-tests.json', payloads)
    (folder / 'statement.md').write_text(f"# {spec['number']:02d}. {spec['title']}\n\n{spec['statement'].strip()}\n")
    (folder / 'Marker.java').write_text(MARKER)
    (folder / 'solution.md').write_text(
        '## Reference solution\n\nUse this implementation above the supplied tests and runner.\n\n'
        f"```python\n{spec['reference'].strip()}\n```\n")
    return result
