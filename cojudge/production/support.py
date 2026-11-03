"""Build concise Python tickets and check them against independent expectations."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

from cojudge.authoring.support import ROOT, check_java, encode, java_source, json_equal, python_solver, write_json
from cojudge.production.guide import CATEGORIES, GUIDES, ORDER
from cojudge.production.presentation import present, solution

HERE = ROOT / 'cojudge/production'
COURSE_ID = 'software-engineering'
COURSE_NUMBERS = [number for number, _ in ORDER]


def load_specs(numbers=None):
    """Load the course tickets in course order, with their learner guides applied."""
    specs = []
    for position, (number, category) in enumerate(ORDER, 1):
        if numbers and number not in numbers:
            continue
        path = HERE / 'tickets' / f'p{number:02d}.py'
        module = importlib.util.module_from_spec(info := importlib.util.spec_from_file_location(f'production_{path.stem}', path))
        info.loader.exec_module(module)
        guide = GUIDES[number]
        spec = {**module.SPEC, 'position': position, 'category': category,
                'starter': guide['starter'], 'hints': guide['hints'],
                'difficulty': guide.get('difficulty', module.SPEC['difficulty'])}
        if 'simple_solution' in guide:
            spec['simple_solution'] = guide['simple_solution']
        specs.append(spec)
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
    for name in ('starter', 'simple_solution'):
        if name not in spec:
            continue
        solver = python_solver(spec[name] + f"\n\ndef solve(data):\n    return {spec['function']}(**data)\n")
        failures = 0
        for case in spec['cases']:
            data = copy.deepcopy(case['input'])
            try:
                failures += not json_equal(solver(data), case['expected']) or not json_equal(data, case['input'])
            except Exception:
                failures += 1
        if name == 'starter':
            assert failures, f"The template must not solve {problem_id(spec)}"
        else:
            assert not failures, f"The explained solution fails {problem_id(spec)}"
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


def present_problem(spec, test_ids):
    return present(spec)


def build_problem(spec, destination):
    report = verify(spec)
    folder = Path(destination) / 'problems' / problem_id(spec)
    folder.mkdir(parents=True, exist_ok=True)
    presentation = present_problem(spec, [])
    metadata = {
        'id': problem_id(spec), 'title': f"{spec['position']:02d}. {spec['title']}",
        'difficulty': spec['difficulty'], 'link': '', 'category': spec['category'],
        'examples': presentation['examples'],
        'testCaseDescriptions': presentation['testCaseDescriptions'],
        'courseHelp': presentation['courseHelp'],
        'starterCode': {'python': full_source(spec, spec['starter'])},
        'testCases': [{'payload': encode(c['input'])} for c in spec['cases'][:3]],
        'functionName': 'run', 'params': [{'name': 'payload', 'type': 'string'}],
        'outputType': 'string', 'hints': spec.get('hints', []),
    }
    write_json(folder / 'metadata.json', metadata)
    write_json(folder / 'official-tests.json', [{'payload': encode(c['input'])} for c in spec['cases']])
    (folder / 'Marker.java').write_text(java_source(verification_spec(spec)))
    (folder / 'statement.md').write_text(presentation['statement'])
    (folder / 'solution.md').write_text(solution(spec))
    return {**report, 'number': spec['number'], 'category': spec['category']}


def course_info(records):
    return {'title': 'Software Engineering Tickets',
            'description': '15 short Python tickets from real services, in four stages: clean input, data and APIs, reliability, and security and money. Each ticket says why it matters and gives step-by-step starter code, three hints, and an explained solution. Each ticket is independent.',
            'category-order': CATEGORIES,
            'problems-of-category': {category: [r['id'] for r in records if r['category'] == category] for category in CATEGORIES}}
