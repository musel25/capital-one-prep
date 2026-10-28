"""Build and verify the FastAPI path with the real framework and real pytest."""
from __future__ import annotations

import ast
import json
import subprocess
import tempfile
from pathlib import Path

from cojudge.authoring.support import ROOT, write_json
from cojudge.fastapi_path.extra_tests import EXTRA
from cojudge.fastapi_path.runner import ADAPTER
from cojudge.fastapi_path.specs import ADDITIONS, AUTH, CONTRACTS, ERROR_CHECKS, HTML_BODY, MUTATIONS
from cojudge.pybites.runner import MARKER
from cojudge.presentation import course_help, statement_text, test_case_details
from cojudge.fastapi_path.presentation import CLARIFICATIONS, EXAMPLES, original_description

HERE = Path(__file__).parent
COURSE_ID = 'pybites-fastapi'


def load_specs(numbers=None):
    pages = json.loads((HERE / 'source-pages.json').read_text())
    specs = []
    for page in pages:
        n = page['n']
        if numbers and n not in numbers:
            continue
        template = page['template'].replace('password=<redacted>', 'password: str')
        template = template.replace('from pydantic import BaseModel\n', 'from pydantic import BaseModel, Field\n')
        template = template.replace('date_added: datetime = datetime.now()', 'date_added: datetime = Field(default_factory=datetime.now)')
        template = template.replace('access_token=<redacted>', 'access_token: str')
        template = template.replace('"<redacted_base64>"', '"classroom-only-signing-key-do-not-use-in-production"')
        template = template.replace('password: str\n    """', 'password: str):\n    """')
        template = template.replace('token=<redacted> = Depends(oauth2_scheme)', 'token: str = Depends(oauth2_scheme)')
        tests = page['tests'].replace('password=<redacted>', 'password=LAME_PASSWORD)')
        tests = tests.replace('token=<redacted>"access_token"]', 'token = data["access_token"]')
        tests = tests.replace('Bearer <redacted>', 'Bearer invalid-example-token')
        tests += '\n\n# Added Cojudge boundary tests.\n' + EXTRA.get(n, '')
        if n <= 7:
            reference = template.replace('app = ...', 'app = FastAPI()') + '\n' + ADDITIONS[n]
        elif n == 8:
            reference = 'from fastapi import HTTPException\n' + template.replace(
                '    # TODO: add exception handling code here', ERROR_CHECKS.rstrip())
        elif n == 9:
            reference = template.rsplit('    pass', 1)[0] + HTML_BODY
        else:
            reference = template.split('def authenticate_user(', 1)[0] + AUTH
        assert '<redacted' not in template + tests + reference, n
        compile(template, f'starter_{n}', 'exec')
        compile(reference, f'reference_{n}', 'exec')
        tree = ast.parse(tests)
        ids = [node.name for node in tree.body if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')]
        specs.append({
            'page': page, 'number': n, 'id': f"pbf-{n:02d}-{page['slug']}", 'title': page['title'],
            'url': page['url'], 'module': 'models' if n in (2, 6) else 'app',
            'template': template, 'tests': tests, 'reference': reference, 'test_ids': ids,
            'contract': CONTRACTS[n - 1], 'mutations': MUTATIONS[n],
            'category': '01-basics' if n <= 2 else '02-food-api' if n <= 5 else '03-food-log' if n <= 9 else '04-authentication',
        })
    return specs


def full_source(spec, code):
    tests = spec['tests'].strip() + '\n'
    assert "'''" not in tests
    return (code.rstrip() + '\n\n# === SUPPLIED FASTAPI TESTS ===\n'
            '# Keep the tests and adapter unchanged.\n'
            f"_FA_MODULE = {spec['module']!r}\n_FA_IDS = {spec['test_ids']!r}\n"
            "_FA_TESTS = r'''\n" + tests + "'''\n" + ADAPTER)


def run_all(spec, code):
    with tempfile.TemporaryDirectory(prefix='verify-fastapi-') as work:
        Path(work, 'Solution.py').write_text(full_source(spec, code))
        script = ("import json\nfrom Solution import Solution\nrun=Solution().run\n"
                  f"print(json.dumps({{name:run(json.dumps({{'test':name}})) for name in {spec['test_ids']!r}}}))")
        done = subprocess.run(['uv', 'run', '--project', str(HERE), '--frozen', 'python', '-c', script],
                              cwd=work, capture_output=True, text=True, timeout=300)
        assert done.returncode == 0, done.stderr[-3000:]
        return json.loads(done.stdout.strip().splitlines()[-1])


def verify(spec):
    good = run_all(spec, spec['reference'])
    failed = {key: value for key, value in good.items() if value != 'passed'}
    assert good and not failed, (spec['id'], failed)
    starter = run_all(spec, spec['template'])
    assert any(value != 'passed' for value in starter.values()), 'Starter passes: ' + spec['id']
    faults = []
    for name, old, new in spec['mutations']:
        assert old in spec['reference'], (spec['id'], name)
        result = run_all(spec, spec['reference'].replace(old, new, 1))
        caught = [key for key, value in result.items() if value != 'passed']
        assert caught, 'Fault survived: ' + name
        faults.append({'name': name, 'detected_by': caught})
    return {'id': spec['id'], 'cases': len(good), 'faults': faults}


def present_problem(spec, test_ids):
    return {
        'statement': statement_text(original_description(spec), CLARIFICATIONS[spec['number']]),
        'examples': [{'input': code, 'output': result} for code, result in EXAMPLES[spec['number']]],
        'testCaseDescriptions': test_case_details(spec['tests'], test_ids),
        'courseHelp': course_help(spec['url'],
            'This path uses real FastAPI and Pydantic 2 with pytest and TestClient. '
            'No server is needed. The imported starter and tests include added boundary '
            'checks named test_added_. Example password fields and the classroom signing '
            'key were restored after export redaction. The signing key and /create_user '
            'route are exercise fixtures. Select Python.'),
    }


def build_problem(spec):
    folder = ROOT / 'cojudge/problems' / spec['id']
    folder.mkdir(parents=True, exist_ok=True)
    # Real pytest and bcrypt need a separate execution budget for each check.
    cases = [{'payload': json.dumps({'test': name}), '_isLargeTest': True} for name in spec['test_ids']]
    presentation = present_problem(spec, spec['test_ids'])
    write_json(folder / 'metadata.json', {
        'id': spec['id'], 'title': f"{spec['number']:02d}. {spec['title']}",
        'difficulty': 'Easy' if spec['number'] <= 2 else 'Hard' if spec['number'] == 10 else 'Medium',
        'category': spec['category'], 'link': '',
        'starterCode': {'python': full_source(spec, spec['template'])},
        **{key: value for key, value in presentation.items() if key != 'statement'},
        'testCases': cases[:3], 'functionName': 'run',
        'params': [{'name': 'payload', 'type': 'string'}], 'outputType': 'string',
        'hints': ['Read the supplied pytest tests.', 'Use the real FastAPI and Pydantic packages.'],
    })
    write_json(folder / 'official-tests.json', cases)
    (folder / 'Marker.java').write_text(MARKER)
    (folder / 'solution.md').write_text('## Reference solution\n\n```python\n' + spec['reference'].strip() + '\n```\n')
    (folder / 'statement.md').write_text(presentation['statement'])


def build(specs):
    for spec in specs:
        build_problem(spec)
    levels = ['01-basics', '02-food-api', '03-food-log', '04-authentication']
    (ROOT / 'cojudge/courses' / COURSE_ID).mkdir(parents=True, exist_ok=True)
    write_json(ROOT / 'cojudge/courses' / COURSE_ID / 'courseinfo.json', {
        'title': 'Pybites FastAPI Path',
        'description': 'The 10 exercises of the Pybites FastAPI learning path, in source order. Build a food and calorie API with real FastAPI, Pydantic, pytest, and JWT authentication. Imported templates and tests, with documented adaptations and added boundary tests. Select Python.',
        'category-order': levels,
        'problems-of-category': {level: [spec['id'] for spec in specs if spec['category'] == level] for level in levels},
    })
