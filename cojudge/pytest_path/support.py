"""Build and verify the Pybites Pytest path as native CoJudge content."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile

from cojudge.authoring.support import ROOT, write_json
from cojudge.pytest_path.runner import ADAPTER, ENGINE, HELPERS, MARKER
from cojudge.pytest_path.specs import SPECS
from cojudge.presentation import course_help, statement_text
from cojudge.pytest_path.presentation import EXAMPLES, RUNNER_HELP, original_description

HERE = ROOT / 'cojudge/pytest_path'
COURSE_ID = 'pybites-pytest'


def load_specs():
    pages = json.loads((HERE / 'source-pages.json').read_text())
    assert len(pages) == len(SPECS) == 10
    result = []
    for item, page in zip(SPECS, pages):
        spec = {**item, 'title': page['title'], 'url': page['url'], 'page': page}
        spec['id'] = f"pbt-{spec['number']:02d}-" + page['url'].rstrip('/').split('/')[-1].replace('_', '-')
        variants = []
        for mutation in spec['mutations']:
            assert mutation['old'] in spec['target'], mutation['name']
            source = spec['target'].replace(mutation['old'], mutation['new'], 1)
            compile(source, spec['module'] + '.py', 'exec')
            variants.append({'name': mutation['name'], 'source': source})
        spec['variants'] = variants
        result.append(spec)
    return result


def checks(spec):
    return ['baseline'] + [item['name'] for item in spec['variants']]


def full_source(spec, tests):
    return ('# Supplied target and offline pytest runner. Keep this section unchanged.\n'
            f"_PT_MODULE = {spec['module']!r}\n_PT_TARGET = {spec['target']!r}\n"
            f"_PT_MUTANTS = {spec['variants']!r}\n" + HELPERS + ENGINE +
            '\n# === WRITE YOUR TESTS BELOW ===\n\n' + tests.rstrip() + '\n' + ADAPTER)


def run_all(spec, tests):
    with tempfile.TemporaryDirectory(prefix='cojudge-pytest-') as work:
        (Path(work) / 'Solution.py').write_text(full_source(spec, tests))
        script = ("import json\nfrom Solution import Solution\nrun = Solution().run\n"
                  f"print(json.dumps({{case: run(json.dumps({{'check': case}})) for case in {checks(spec)!r}}}))\n")
        done = subprocess.run(['uv', 'run', '--python', '3.11', '--no-project', 'python', '-c', script],
                              cwd=work, capture_output=True, text=True, timeout=60)
        if done.returncode:
            raise AssertionError(f"{spec['id']}: runner crashed\n{done.stderr[-3000:]}")
        return json.loads(done.stdout.strip().splitlines()[-1])


def verify(spec):
    results = run_all(spec, spec['reference'])
    assert results and all(result == 'passed' for result in results.values()), (spec['id'], results)
    starter = run_all(spec, spec['starter'])
    assert starter['baseline'] != 'passed', spec['id']
    return {'id': spec['id'], 'checks': len(results), 'faults': len(spec['variants'])}


def present_problem(spec, test_ids):
    target = spec['target'].strip()
    task = (original_description(spec) + '\n\n'
            'For this version, write tests for the supplied code. Your tests must pass against the correct '
            'code, cover at least 90% of its executable statements, and detect every '
            'supplied faulty version. A fault is detected when at least one test fails. '
            'An empty test suite does not pass.\n\n'
            f'Import the target as `{spec["module"]}`. The judge supplies it automatically.\n\n'
            f'```python\n{target}\n```')
    details = {'baseline': {'title': 'Correct code: tests pass and cover at least 90%', 'code': target}}
    details.update({variant['name']: {
        'title': 'Detect fault: ' + variant['name'], 'code': variant['source'].strip()
    } for variant in spec['variants']})
    origin = ('The Fibonacci target is the original code visible on Pybites.' if spec['number'] == 1 else
              'This target and its tests are an offline recreation from the public description. '
              'The original code and template require Pybites premium.')
    return {
        'statement': statement_text(task),
        'examples': [{'input': f'from {spec["module"]} import *\n' + code, 'output': result}
                     for code, result in EXAMPLES[spec['number']]],
        'testCaseDescriptions': {test_id: details[test_id] for test_id in test_ids},
        'courseHelp': course_help(spec['url'], origin + '\n\n' + RUNNER_HELP, testing=True),
    }


def statement(spec):
    return present_problem(spec, checks(spec))['statement']


def build(destination=ROOT / 'cojudge'):
    specs = load_specs()
    records = []
    for spec in specs:
        record = verify(spec)
        folder = Path(destination) / 'problems' / spec['id']
        folder.mkdir(parents=True, exist_ok=True)
        cases = [{'payload': json.dumps({'check': case})} for case in checks(spec)]
        presentation = present_problem(spec, checks(spec))
        metadata = {
            'id': spec['id'], 'title': f"{spec['number']:02d}. {spec['title']}",
            'difficulty': 'Easy' if spec['number'] <= 3 else 'Medium' if spec['number'] <= 6 else 'Hard',
            'link': '', 'category': 'pytest',
            **{key: value for key, value in presentation.items() if key != 'statement'},
            'starterCode': {'python': full_source(spec, spec['starter'])},
            'testCases': cases[:3], 'functionName': 'run',
            'params': [{'name': 'payload', 'type': 'string'}], 'outputType': 'string',
            'hints': ['Read the supplied code and contract before writing tests.',
                      'Test boundaries, invalid input, and state changes.',
                      'A SURVIVED result names a fault that your suite must detect.'],
        }
        write_json(folder / 'metadata.json', metadata)
        write_json(folder / 'official-tests.json', cases)
        (folder / 'Marker.java').write_text(MARKER)
        (folder / 'statement.md').write_text(presentation['statement'])
        (folder / 'solution.md').write_text('## Reference tests\n\n```python\n' + spec['reference'] + '```\n')
        records.append(record)
    course = Path(destination) / 'courses' / COURSE_ID
    course.mkdir(parents=True, exist_ok=True)
    write_json(course / 'courseinfo.json', {
        'title': 'Pybites Pytest Path',
        'description': 'The 10 exercises of the Pybites Pytest learning path, in the original order. '
            'Write tests that pass against correct code and detect supplied faulty variants. '
            'Fibonacci uses the original visible code. Exercises 2–10 are labeled offline recreations '
            'from public descriptions. Uses the OOP course’s small pytest subset, statement coverage, '
            'and explicit faults; not pytest-cov or mutatest. Select Python.',
        'category-order': ['pytest'], 'problems-of-category': {'pytest': [spec['id'] for spec in specs]},
    })
    return records
