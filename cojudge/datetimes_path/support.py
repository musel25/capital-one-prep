"""Build the Datetimes and Timezones path with the established Pybites Python runner."""
import json
from pathlib import Path

from cojudge.authoring.support import ROOT, write_json
from cojudge.pybites.runner import MARKER
from cojudge.pybites.support import description, full_source, run_all

COURSE_ID = 'pybites-datetimes-timezones'
HERE = Path(__file__).parent


def problem_id(spec):
    return f"pbd-{spec['number']:02d}-{spec['page']['slug']}"


def load_specs(numbers=None):
    from cojudge.datetimes_path.bites import SPECS
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
    levels = [('01-beginner', 'Beginner'), ('02-intermediate', 'Intermediate'), ('03-advanced', 'Advanced')]
    return {
        'title': 'Pybites Datetimes and Timezones Path',
        'description': 'All 24 exercises from the Pybites Datetimes and Timezones learning path, in source order. '
                       'The two free exercises retain their original templates and tests. The other exercises '
                       'use recreated templates and tests. Data is supplied offline. Select Python.',
        'category-order': [category for category, _ in levels],
        'problems-of-category': {category: [problem_id(s) for s in specs if s['page']['level'] == level]
                                 for category, level in levels},
    }


def statement(spec, count):
    page = spec['page']
    source_description = '\n'.join(line.rstrip() for line in description(spec).splitlines())
    origin = ('This version keeps the original free template and tests, with added boundary tests.'
              if spec.get('original') else
              'The premium template and tests are not available in this account. '
              'This version uses a recreated template and tests based on the public description.')
    if spec.get('adapted'):
        origin = spec['adapted']
    return f"""# {spec['number']:02d}. {spec['title']}

[Course list](/?course={COURSE_ID}) · [Original bite](https://pybitesplatform.com/bites/{page['slug']}/)

{spec['contract']}

**Source and offline changes:** {origin}

<details>
<summary>Original public description</summary>

{source_description}

</details>

Write your implementation at the top of the editor. The tests below it import your code as
`{spec['module']}`. **Run** checks the first three tests. **Submit** checks all {count} tests.
A failed test shows its name, error, and test line.

- Python 3.11. Use the standard library. All required data is supplied. No network access.
- Keep the supplied tests and runner. Implement the functions above them.
- For a saved solution, use **+** beside the editor tabs to open the current template in a new tab.
"""


def build_problem(spec, destination=ROOT / 'cojudge'):
    result = verify(spec)
    folder = Path(destination) / 'problems' / result['id']
    folder.mkdir(parents=True, exist_ok=True)
    payloads = [json.dumps({'test': test}) for test in result['tests']]
    metadata = {
        'id': result['id'], 'title': f"{spec['number']:02d}. {spec['title']}",
        'difficulty': {'Beginner': 'Easy', 'Intermediate': 'Medium', 'Advanced': 'Hard'}[spec['page']['level']],
        'link': '',
        'category': {'Beginner': '01-beginner', 'Intermediate': '02-intermediate', 'Advanced': '03-advanced'}[spec['page']['level']],
        'examples': [{'input': p, 'output': 'passed'} for p in payloads[:3]],
        'starterCode': {'python': full_source(spec, spec['template'])},
        'testCases': [{'payload': p} for p in payloads[:3]],
        'functionName': 'run', 'params': [{'name': 'payload', 'type': 'string'}],
        'outputType': 'string', 'hints': spec.get('hints', []),
    }
    write_json(folder / 'metadata.json', metadata)
    write_json(folder / 'official-tests.json', [{'payload': p} for p in payloads])
    (folder / 'statement.md').write_text(statement(spec, result['cases']))
    (folder / 'Marker.java').write_text(MARKER)
    (folder / 'solution.md').write_text(
        f"## Reference solution\n\nPaste this code above the supplied tests and runner.\n\n"
        f"```python\n{spec['reference'].strip()}\n```\n")
    return result
