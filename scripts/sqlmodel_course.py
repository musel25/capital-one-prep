"""Build, verify, and check the SQLModel path on the live judge."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import ROOT, write_json
from cojudge.sqlmodel_path.support import build_problem, course_info, full_source, load_specs, problem_id, test_ids, verify
from scripts.pybites_course import submit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify', 'live'])
    parser.add_argument('--only', nargs='+', type=int)
    parser.add_argument('--base-url')
    parser.add_argument('--user', default='musel')
    args = parser.parse_args()
    if args.command == 'live' and not args.base_url:
        parser.error('live needs --base-url')
    specs = load_specs(args.only)
    records, failures = [], []
    for spec in specs:
        try:
            if args.command == 'build':
                result = build_problem(spec)
            elif args.command == 'verify':
                result = verify(spec)
            else:
                pid = problem_id(spec)
                good = submit(args.base_url, args.user, pid, full_source(spec, spec['reference']))
                assert good.get('accepted') and good.get('totalTc') == len(test_ids(spec)), str(good)[:2500]
                bad = submit(args.base_url, args.user, pid, full_source(spec, spec['template']))
                assert not bad.get('accepted'), f'{pid}: starter accepted'
                result = {'id': pid, 'cases': good['totalTc']}
            records.append(result)
            print(f"PASS {result['id']} ({result['cases']} tests)", flush=True)
        except Exception as error:
            failures.append({'number': spec['number'], 'error': str(error)})
            print(f"FAIL {spec['number']:02d}: {error}", flush=True)
    if args.command == 'build' and not args.only and not failures:
        course = ROOT / 'cojudge/courses/pybites-sqlmodel'
        course.mkdir(parents=True, exist_ok=True)
        write_json(course / 'courseinfo.json', course_info(specs))
    write_json(ROOT / f'cojudge/sqlmodel_path/{args.command}-report.json', {'passed': records, 'failed': failures})
    print(f'{len(records)} passed; {len(failures)} failed.')
    raise SystemExit(bool(failures))


if __name__ == '__main__':
    main()
