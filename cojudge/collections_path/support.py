"""Build the Collections path with the established Pybites Python runner."""
import json
from pathlib import Path

from cojudge.authoring.support import ROOT, write_json
from cojudge.pybites.runner import MARKER
from cojudge.pybites.support import description, full_source, run_all
from cojudge.presentation import course_help, statement_text, test_case_details
from cojudge.collections_path.examples import ASSUMPTIONS, examples

COURSE_ID = 'pybites-collections'
HERE = Path(__file__).parent


def problem_id(spec):
    return f"pbc-{spec['number']:02d}-{spec['page']['slug']}"


def load_specs(numbers=None):
    from cojudge.collections_path.bites import SPECS
    pages = [{key: value.replace('\r\n', '\n') if isinstance(value, str) else value
              for key, value in page.items()}
             for page in json.loads((HERE / 'source-pages.json').read_text())]
    return [{**spec, 'number': page['n'], 'page': page}
            for spec, page in zip(SPECS, pages, strict=True)
            if not numbers or page['n'] in numbers]


def verify(spec):
    results = run_all(spec, spec['reference'])
    failures = {name: result for name, result in results.items() if result != 'passed'}
    assert results and not failures, f"{problem_id(spec)} reference fails: {failures}"
    starter = run_all(spec, spec['template'])
    assert any(value != 'passed' for value in starter.values()), 'Starter passed all tests'
    mutations = []
    for fault in spec['mutations']:
        assert fault['old'] in spec['reference'], f"Missing mutation: {fault['name']}"
        source = spec['reference'].replace(fault['old'], fault['new'], 1)
        compile(source, '<fault>', 'exec')
        faulty = run_all(spec, source)
        detected = [name for name, result in faulty.items() if result != 'passed']
        assert detected, f"Mutation survived: {fault['name']}"
        mutations.append({'name': fault['name'], 'detected_by': detected})
    return {'id': problem_id(spec), 'cases': len(results), 'tests': list(results),
            'template_failures': sum(value != 'passed' for value in starter.values()),
            'mutations': mutations}


def course_info(specs):
    return {
        'title': 'Pybites Collections Path',
        'description': 'The 11 exercises from the Pybites Collections Module learning path, '
                       'in their original order. Practice namedtuple, deque, defaultdict, and Counter. '
                       'Free exercises retain their original tests. Premium exercises use '
                       'recreated templates and tests. Data is supplied offline. Select Python.',
        'category-order': ['01-beginner', '02-intermediate'],
        'problems-of-category': {
            category: [problem_id(s) for s in specs if s['page']['level'] == level]
            for category, level in [('01-beginner', 'Beginner'), ('02-intermediate', 'Intermediate')]},
    }


def present_problem(spec, test_ids):
    page = spec['page']
    origin = ('This version keeps the original free template and tests, with added boundary tests.'
              if spec.get('original') else
              'The template and tests are recreations based on the public description.')
    origin = spec.get('adapted', origin)
    note = ' '.join(filter(None, [origin, spec.get('notes'),
                                 'Python 3.11. Data is supplied offline. Use the standard library.']))
    return {
        'statement': statement_text(description(spec), ASSUMPTIONS.get(spec['number'], ())),
        'examples': examples(spec['number']),
        'testCaseDescriptions': test_case_details(spec['tests'], test_ids),
        'courseHelp': course_help(f"https://pybitesplatform.com/bites/{page['slug']}/", note),
    }


def statement(spec, count):
    return present_problem(spec, [])['statement']


def build_problem(spec, destination=ROOT / 'cojudge'):
    result = verify(spec)
    folder = Path(destination) / 'problems' / result['id']
    folder.mkdir(parents=True, exist_ok=True)
    payloads = [json.dumps({'test': test}) for test in result['tests']]
    presentation = present_problem(spec, result['tests'])
    metadata = {
        'id': result['id'], 'title': f"{spec['number']:02d}. {spec['title']}",
        'difficulty': 'Easy' if spec['page']['level'] == 'Beginner' else 'Medium',
        'link': '',
        'category': '01-beginner' if spec['page']['level'] == 'Beginner' else '02-intermediate',
        'examples': presentation['examples'],
        'testCaseDescriptions': presentation['testCaseDescriptions'],
        'courseHelp': presentation['courseHelp'],
        'starterCode': {'python': full_source(spec, spec['template'])},
        'testCases': [{'payload': p} for p in payloads[:3]],
        'functionName': 'run', 'params': [{'name': 'payload', 'type': 'string'}],
        'outputType': 'string', 'hints': spec.get('hints', []),
    }
    write_json(folder / 'metadata.json', metadata)
    write_json(folder / 'official-tests.json', [{'payload': p} for p in payloads])
    (folder / 'statement.md').write_text(presentation['statement'])
    (folder / 'Marker.java').write_text(MARKER)
    (folder / 'solution.md').write_text(
        f"## Reference solution\n\nPaste this code above the supplied tests and runner.\n\n"
        f"```python\n{spec['reference'].strip()}\n```\n")
    return result
