"""Build and verify native Cojudge content using the locked SQLModel environment."""
import ast
import json
from pathlib import Path
import subprocess
import tempfile

from cojudge.authoring.support import ROOT, write_json
from .runner import RUNNER, SENTINEL, MARKER
from cojudge.presentation import course_help, statement_text, test_case_details
from .presentation import CLARIFICATIONS, EXAMPLES

HERE = Path(__file__).parent.resolve()
COURSE_ID = 'pybites-sqlmodel'
CATEGORIES = ['01-tables-and-crud', '02-relationships-and-schemas', '03-fastapi']


def load_specs(numbers=None):
    from .bites import SPECS as basic
    from .relationships import SPECS as relations
    from .api import SPECS as api
    pages = {p['n']: p for p in json.loads((HERE / 'source-pages.json').read_text())}
    return [{**s, 'page': pages[s['number']], 'title': pages[s['number']]['title']}
            for s in [*basic, *relations, *api] if not numbers or s['number'] in numbers]


def problem_id(spec):
    return f"pbs-{spec['number']:02d}-{spec['page']['slug']}"


def test_ids(spec):
    return [node.name for node in ast.parse(spec['tests']).body
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')]


def full_source(spec, code):
    tests = spec['tests'].strip('\n') + '\n'
    quote = "'''" if "'''" not in tests else '"""'
    block = f'r{quote}\n{tests}{quote}[1:]'
    return (code.rstrip() + '\n\n' + SENTINEL + '\n'
            '# Read the tests below. Keep the supplied tests and runner.\n'
            f"_SM_TESTS = {block}\n_SM_IDS = {test_ids(spec)!r}\n" + RUNNER)


def run_all(spec, code, target=None):
    with tempfile.TemporaryDirectory(prefix='sqlmodel-verify-') as folder:
        (Path(folder) / 'Solution.py').write_text(full_source(spec, code))
        script = ('import json\nfrom Solution import Solution\nrun=Solution().run\n' +
                  ('print(json.dumps(run(' + repr(json.dumps({'test': target})) + ')))\n' if target else
                   'ids=json.loads(run(json.dumps({"test":"--list"})))\n'
                   'print(json.dumps({name:run(json.dumps({"test":name})) for name in ids}))\n'))
        done = subprocess.run(['uv', 'run', '--project', str(HERE), '--frozen', 'python', '-c', script],
                              cwd=folder, capture_output=True, text=True, timeout=40)
        assert done.returncode == 0, f"{problem_id(spec)} crashed: {done.stderr[-3000:]}"
        return json.loads(done.stdout.strip().splitlines()[-1])


def verify(spec):
    results = run_all(spec, spec['reference'])
    failures = {name: result for name, result in results.items() if result != 'passed'}
    assert results and not failures, f"{problem_id(spec)}: {failures}"
    starter = run_all(spec, spec['template'])
    assert any(value != 'passed' for value in starter.values()), 'Starter passes all tests'
    faults = []
    for mutation in spec['mutations']:
        assert mutation['old'] in spec['reference'], f"Missing fault: {mutation['name']}"
        code = spec['reference'].replace(mutation['old'], mutation['new'], 1)
        compile(code, '<fault>', 'exec')
        detected = [name for name, result in run_all(spec, code).items() if result != 'passed']
        assert detected, f"Fault survived: {problem_id(spec)}: {mutation['name']}"
        faults.append({'name': mutation['name'], 'detected_by': detected})
    return {'id': problem_id(spec), 'cases': len(results), 'tests': list(results),
            'template_failures': sum(v != 'passed' for v in starter.values()), 'mutations': faults}


def category(spec):
    return CATEGORIES[0 if spec['number'] <= 4 else 1 if spec['number'] <= 8 else 2]


def course_info(specs):
    return {'title': 'Pybites SQLModel Path',
            'description': 'The 10 SQLModel learning path exercises, in the original order. Build a workout '
            'tracker with real SQLModel, SQLite, relationships, API schemas, and FastAPI. All templates '
            'and tests are recreations based on the public descriptions. The original exercises require '
            'Pybites premium. Select Python. The supplied runtime includes all required packages.',
            'category-order': CATEGORIES,
            'problems-of-category': {c: [problem_id(s) for s in specs if category(s) == c] for c in CATEGORIES}}


def present_problem(spec, test_ids):
    return {
        'statement': statement_text(spec['page']['description'], CLARIFICATIONS[spec['number']]),
        'examples': [{'input': code, 'output': result} for code, result in EXAMPLES[spec['number']]],
        'testCaseDescriptions': test_case_details(spec['tests'], test_ids),
        'courseHelp': course_help(f"https://pybitesplatform.com/bites/{spec['page']['slug']}/",
            'These templates and tests are recreations from the public descriptions. '
            'The original templates and tests require Pybites premium. The runtime supplies '
            'SQLModel, SQLite, SQLAlchemy, Pydantic, FastAPI, HTTPX, and pytest. Each check '
            'uses a separate database. No server is needed. Select Python.'),
    }


def statement(spec, count):
    return present_problem(spec, test_ids(spec))['statement']


def build_problem(spec, destination=ROOT / 'cojudge'):
    result = verify(spec)
    folder = Path(destination) / 'problems' / result['id']
    folder.mkdir(parents=True, exist_ok=True)
    payloads = [json.dumps({'test': name}) for name in result['tests']]
    presentation = present_problem(spec, result['tests'])
    metadata = {'id': result['id'], 'title': f"{spec['number']:02d}. {spec['title']}",
                'difficulty': 'Easy' if spec['number'] <= 4 else 'Medium' if spec['number'] <= 8 else 'Hard',
                'link': '', 'category': category(spec),
                **{key: value for key, value in presentation.items() if key != 'statement'},
                'starterCode': {'python': full_source(spec, spec['template'])},
                'testCases': [{'payload': p} for p in payloads[:3]],
                'functionName': 'run', 'params': [{'name': 'payload', 'type': 'string'}],
                'outputType': 'string', 'hints': []}
    write_json(folder / 'metadata.json', metadata)
    write_json(folder / 'official-tests.json', [{'payload': p} for p in payloads])
    (folder / 'statement.md').write_text(presentation['statement'])
    (folder / 'Marker.java').write_text(MARKER)
    (folder / 'solution.md').write_text('## Reference solution\n\nPaste this implementation above the supplied tests.\n\n```python\n' + spec['reference'].strip() + '\n```\n')
    return result
