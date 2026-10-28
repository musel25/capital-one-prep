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
            'number': n, 'id': f"pbf-{n:02d}-{page['slug']}", 'title': page['title'],
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


def build_problem(spec):
    folder = ROOT / 'cojudge/problems' / spec['id']
    folder.mkdir(parents=True, exist_ok=True)
    # Real pytest and bcrypt need a separate execution budget for each check.
    cases = [{'payload': json.dumps({'test': name}), '_isLargeTest': True} for name in spec['test_ids']]
    write_json(folder / 'metadata.json', {
        'id': spec['id'], 'title': f"{spec['number']:02d}. {spec['title']}",
        'difficulty': 'Easy' if spec['number'] <= 2 else 'Hard' if spec['number'] == 10 else 'Medium',
        'category': spec['category'], 'link': '',
        'starterCode': {'python': full_source(spec, spec['template'])},
        'examples': [{'input': case['payload'], 'output': 'passed'} for case in cases[:3]],
        'testCases': cases[:3], 'functionName': 'run',
        'params': [{'name': 'payload', 'type': 'string'}], 'outputType': 'string',
        'hints': ['Read the supplied pytest tests.', 'Use the real FastAPI and Pydantic packages.'],
    })
    write_json(folder / 'official-tests.json', cases)
    (folder / 'Marker.java').write_text(MARKER)
    (folder / 'solution.md').write_text('## Reference solution\n\n```python\n' + spec['reference'].strip() + '\n```\n')
    (folder / 'statement.md').write_text(f'''# {spec['number']:02d}. {spec['title']}

[Course list](/?course={COURSE_ID}) · [Original Pybites exercise]({spec['url']})

## Required behavior

{spec['contract']}

## How to solve it

Use Python. Write your solution at the top of the editor. The supplied tests follow it.
Run checks up to three tests. Submit checks all {len(cases)} tests.
Each check runs real pytest and FastAPI in a fresh process. No server or network is needed.
Keep the supplied tests and adapter unchanged. Failures show the pytest test name and error.

## Source and changes

The starter and tests were imported from the exercise pages accessible in the user's Pybites session.
Example password fields and the classroom signing key were restored with explicit test values after export redaction.
FoodEntry uses a per-instance timestamp default. Tests labelled `test_added_` are added Cojudge checks.
The required behavior above summarizes the source description and states the added checks.
The reference solution was written for this course.

The runtime uses Python 3.11, FastAPI 0.161.1, Pydantic 2, real pytest,
HTTPX, Passlib/bcrypt, python-jose, python-multipart, and BeautifulSoup.
Package versions are locked in `cojudge/fastapi_path/uv.lock` in the content repository.

For an old saved solution, use **+** beside the editor tabs to open the current starter.
Copy your code into that tab. Keep your old saved tab.
''')


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
