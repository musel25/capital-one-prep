"""Build concise Python tickets and check them against independent expectations."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

from cojudge.authoring.support import ROOT, check_java, encode, java_source, json_equal, python_solver, write_json

HERE = ROOT / 'cojudge/production'
COURSE_ID = 'software-engineering'
CATEGORIES = ['01-data-and-api', '02-clients-and-reliability', '03-stateful-services',
              '04-jobs-and-storage', '05-files-time-and-boundaries', '06-application-logic']


def load_specs(numbers=None):
    specs = []
    for path in sorted((HERE / 'tickets').glob('p[0-9][0-9].py')):
        if numbers and int(path.stem[1:]) not in numbers:
            continue
        module = importlib.util.module_from_spec(info := importlib.util.spec_from_file_location(f'production_{path.stem}', path))
        info.loader.exec_module(module)
        specs.append(module.SPEC)
    return specs


def problem_id(spec):
    return f"pe-{spec['number']:02d}-{spec['slug']}"


def verification_spec(spec):
    return {**spec, 'prefix': 'pe', 'generated': [],
            'reference': spec['reference'] + f"\n\ndef solve(data):\n    return {spec['function']}(**data)\n"}


def full_source(spec, source):
    return source.rstrip() + f'''


# Supplied CoJudge adapter. Implement {spec['function']} above.
class Solution:
    def run(self, payload: str) -> str:
        import json
        data = json.loads(payload)
        before = json.dumps(data, sort_keys=True, ensure_ascii=True, allow_nan=False)
        result = {spec['function']}(**data)
        if json.dumps(data, sort_keys=True, ensure_ascii=True, allow_nan=False) != before:
            raise ValueError("Do not modify the input objects")
        return json.dumps(result, ensure_ascii=True, allow_nan=False)
'''


def verify(spec, java_dir=None):
    assert len(spec['cases']) >= 12, 'Need at least twelve manually expected cases'
    inputs = [encode(c['input']) for c in spec['cases']]
    assert len(inputs) == len(set(inputs)), f"Duplicate inputs in {problem_id(spec)}"
    wrapped = verification_spec(spec)
    solve = python_solver(wrapped['reference'])
    for case in spec['cases'] + list(reversed(spec['cases'])):
        data = copy.deepcopy(case['input'])
        actual = solve(data)
        assert json_equal(data, case['input']), f"Input mutated: {problem_id(spec)} {case['label']}"
        assert json_equal(actual, case['expected']), f"{problem_id(spec)} {case['label']}: {actual!r} != {case['expected']!r}"
    starter = python_solver(spec['starter'] + f"\n\ndef solve(data):\n    return {spec['function']}(**data)\n")
    try:
        starter(copy.deepcopy(spec['cases'][0]['input']))
    except NotImplementedError:
        pass
    else:
        raise AssertionError('The template must not solve the ticket')
    mutations = []
    for mutation in spec['mutations']:
        assert mutation['old'] in spec['reference'], f"Missing mutation target: {mutation['name']}"
        faulty = spec['reference'].replace(mutation['old'], mutation['new'], mutation.get('count', 1))
        bad = python_solver(verification_spec({**spec, 'reference': faulty})['reference'])
        detected = []
        for case in spec['cases']:
            data = copy.deepcopy(case['input'])
            try:
                actual = bad(data)
                if not json_equal(actual, case['expected']) or not json_equal(data, case['input']):
                    detected.append(case['label'])
            except Exception:
                detected.append(case['label'])
        assert detected, f"{problem_id(spec)} mutation survived: {mutation['name']}"
        mutations.append({'name': mutation['name'], 'detected_by': detected})
    report = {'id': problem_id(spec), 'cases': len(spec['cases']), 'mutations': mutations}
    if java_dir is not None:
        report['java'] = check_java(wrapped, java_dir)
    return report


def build_problem(spec, destination):
    report = verify(spec)
    folder = Path(destination) / 'problems' / problem_id(spec)
    folder.mkdir(parents=True, exist_ok=True)
    metadata = {
        'id': problem_id(spec), 'title': f"{spec['number']:02d}. {spec['title']}",
        'difficulty': spec['difficulty'], 'link': '', 'category': spec['category'],
        'examples': [{'input': json.dumps(c['input']), 'output': json.dumps(c['expected']), 'explanation': c['label']}
                     for c in spec['cases'][:3]],
        'starterCode': {'python': full_source(spec, spec['starter'])},
        'testCases': [{'payload': encode(c['input'])} for c in spec['cases'][:3]],
        'functionName': 'run', 'params': [{'name': 'payload', 'type': 'string'}],
        'outputType': 'string', 'hints': spec.get('hints', []),
    }
    write_json(folder / 'metadata.json', metadata)
    write_json(folder / 'official-tests.json', [{'payload': encode(c['input'])} for c in spec['cases']])
    (folder / 'Marker.java').write_text(java_source(verification_spec(spec)))
    (folder / 'statement.md').write_text(
        f"{spec['ticket']}\n\n{spec['task'].strip()}\n\n"
        '**Constraints:**\n\n' + '\n'.join('- ' + c for c in spec['constraints']) +
        '\n- Do not change the input objects. Each call starts with fresh state.\n'
        '- Python 3.11. Standard library only.\n\n'
        f"Implement `{spec['function']}`. **Run** checks the examples. **Submit** checks all {report['cases']} cases.\n"
    )
    (folder / 'solution.md').write_text(f"## Reference solution\n\n```python\n{spec['reference'].strip()}\n```\n")
    return {**report, 'number': spec['number'], 'category': spec['category']}


def course_info(records):
    return {'title': 'Software Engineering Tickets',
            'description': '24 practical Python tickets with a clear input/output contract. Practice validation, APIs, retries, state, SQL, files, timestamps, permissions, version handling, dependencies, synchronization, and safe HTML output. Run checks examples. Submit checks edge cases. Each ticket is independent.',
            'category-order': CATEGORIES,
            'problems-of-category': {category: [r['id'] for r in records if r['category'] == category] for category in CATEGORIES}}
