"""Refresh custom problem text and examples without rebuilding judge files."""
import argparse
import hashlib
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import ROOT, write_json

COURSES = {
    'pybites-oop': 'pybites', 'pybites-collections': 'collections_path',
    'pybites-data-formats': 'data_formats', 'pybites-datetimes-timezones': 'datetimes_path',
    'pybites-fastapi': 'fastapi_path', 'pybites-sqlmodel': 'sqlmodel_path',
    'pybites-typer': 'typer_path', 'pybites-pytest': 'pytest_path',
    'software-engineering': 'production',
}
PRESENTATION_FIELDS = ('examples', 'testCaseDescriptions', 'courseHelp')


def refresh_problem(folder, presentation, *, check=False):
    folder = Path(folder)
    metadata = json.loads((folder / 'metadata.json').read_text())
    for key in PRESENTATION_FIELDS:
        metadata[key] = presentation[key]
    if check:
        assert json.loads((folder / 'metadata.json').read_text()) == metadata, f'Stale metadata: {folder.name}'
        assert (folder / 'statement.md').read_text() == presentation['statement'], f'Stale statement: {folder.name}'
    else:
        write_json(folder / 'metadata.json', metadata)
        (folder / 'statement.md').write_text(presentation['statement'])


def judge_fingerprint(folder):
    metadata = json.loads((folder / 'metadata.json').read_text())
    for key in PRESENTATION_FIELDS:
        metadata.pop(key, None)
    digest = hashlib.sha256(json.dumps(metadata, sort_keys=True).encode())
    for file in sorted(folder.rglob('*')):
        if file.is_file() and file.name not in ('metadata.json', 'statement.md'):
            digest.update(str(file.relative_to(folder)).encode())
            digest.update(file.read_bytes())
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--only', nargs='+', choices=COURSES)
    args = parser.parse_args()
    total = 0
    for course_id in args.only or COURSES:
        module = importlib.import_module(f'cojudge.{COURSES[course_id]}.support')
        specs = module.load_specs()
        expected = json.loads((ROOT / 'cojudge/courses' / course_id / 'courseinfo.json').read_text())
        ids = {pid for values in expected['problems-of-category'].values() for pid in values}
        seen = set()
        for spec in specs:
            pid = module.problem_id(spec) if hasattr(module, 'problem_id') else spec['id']
            assert pid in ids, f'{pid} is outside {course_id}'
            folder = ROOT / 'cojudge/problems' / pid
            before = judge_fingerprint(folder)
            official = json.loads((folder / 'official-tests.json').read_text())
            test_ids = []
            for case in official:
                payload = json.loads(case['payload'])
                if isinstance(payload, dict) and isinstance(selector := payload.get('test', payload.get('check')), str):
                    test_ids.append(selector)
            presentation = module.present_problem(spec, test_ids)
            assert presentation['examples'], f'Missing examples: {pid}'
            assert all(example['output'].strip() != 'passed' for example in presentation['examples']), f'Opaque examples: {pid}'
            assert all(test_id in presentation['testCaseDescriptions'] for test_id in test_ids), f'Missing check descriptions: {pid}'
            refresh_problem(folder, presentation, check=args.check)
            assert judge_fingerprint(folder) == before, f'Judge content changed: {pid}'
            seen.add(pid)
        assert seen == ids, f'Incomplete course: {course_id}'
        total += len(seen)
        print(f'{course_id}: {len(seen)} presentations; judge files unchanged', flush=True)
    print(f'{total} problem presentations {"verified" if args.check else "updated"}.')


if __name__ == '__main__':
    main()
