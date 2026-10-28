"""Build, verify, or check the production engineering tickets on CoJudge."""
import argparse
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import ROOT, write_json
from cojudge.production.support import COURSE_ID, build_problem, course_info, full_source, load_specs, problem_id, verify
from scripts.pybites_course import submit


def rejection_kind(response):
    """A fault can cause a wrong result or a runtime error in the learner function."""
    assert not response.get('accepted'), f'Fault accepted: {response}'
    if any(result.get('isCorrect') is False for result in response.get('results', [])):
        return 'wrong_answer'
    error = response.get('error', '')
    if response.get('errorTestCase') and 'Traceback' in error and 'File "/app/Solution.py"' in error:
        return 'runtime_error'
    raise AssertionError(f'Judge did not reject a learner fault: {response}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['verify', 'build', 'live'])
    parser.add_argument('--only', nargs='+', type=int)
    parser.add_argument('--base-url')
    parser.add_argument('--user', default='musel')
    args = parser.parse_args()
    specs = load_specs(args.only)
    if not args.only and [s['number'] for s in specs] != list(range(1, 25)):
        parser.error('The complete course must contain tickets 01–24')
    records = []
    with tempfile.TemporaryDirectory(prefix='production-java-') as work:
        for spec in specs:
            if args.command == 'verify':
                record = verify(spec, work)
            elif args.command == 'build':
                record = build_problem(spec, ROOT / 'cojudge')
            else:
                if not args.base_url:
                    parser.error('live requires --base-url')
                good = submit(args.base_url, args.user, problem_id(spec), full_source(spec, spec['reference']))
                assert good.get('accepted') and good.get('totalTc') == len(spec['cases']), str(good)[:2000]
                for mutation in spec['mutations']:
                    faulty = spec['reference'].replace(mutation['old'], mutation['new'], mutation.get('count', 1))
                    bad = submit(args.base_url, args.user, problem_id(spec), full_source(spec, faulty))
                    rejection_kind(bad)
                record = {'id': problem_id(spec), 'cases': len(spec['cases'])}
            records.append(record)
            print(f"PASS {record['id']} ({record['cases']} cases)", flush=True)
    if args.command == 'build' and not args.only:
        folder = ROOT / 'cojudge/courses' / COURSE_ID
        folder.mkdir(parents=True, exist_ok=True)
        write_json(folder / 'courseinfo.json', course_info(records))
    print(f'{len(records)} tickets passed.')


if __name__ == '__main__':
    main()
