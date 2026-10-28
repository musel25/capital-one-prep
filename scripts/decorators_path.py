"""Build, verify, and check the 12-exercise decorators course on the real judge."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import ROOT, write_json
from cojudge.decorators_path.support import (
    COURSE_ID, build_problem, course_info, full_source, load_specs, problem_id, run_all, verify,
)
from scripts.pybites_course import submit


def check_live(spec, base_url, user, faults=False):
    pid = problem_id(spec)
    expected = len(run_all(spec, spec['reference']))
    good = submit(base_url, user, pid, full_source(spec, spec['reference']))
    assert good.get('accepted') and good.get('totalTc') == expected, f'{pid} reference: {str(good)[:1800]}'
    bad = submit(base_url, user, pid, full_source(spec, spec['template']))
    assert bad.get('accepted') is False, f'{pid} starter accepted: {str(bad)[:1000]}'
    assert bad.get('totalTc') == expected and any(
        row.get('isCorrect') is False and row.get('output', '').startswith('FAILED ')
        for row in bad.get('results', [])
    ), f'{pid} starter did not produce a test failure: {str(bad)[:1000]}'
    for fault in spec['mutations'] if faults else []:
        code = spec['reference'].replace(fault['old'], fault['new'], fault.get('count', 1))
        result = submit(base_url, user, pid, full_source(spec, code))
        assert result.get('accepted') is False, f"{pid} fault accepted: {fault['name']}"
        # A process error does not prove that a faulty implementation is detected.
        assert result.get('totalTc') == expected, f"{pid} fault did not finish: {fault['name']} {str(result)[:1000]}"
        assert any(row.get('isCorrect') is False and row.get('output', '').startswith('FAILED ')
                   for row in result.get('results', [])), f"{pid} fault produced no test failure: {fault['name']}"
    return {'id': pid, 'cases': expected, 'faults_rejected': len(spec['mutations']) if faults else 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify', 'live'])
    parser.add_argument('--only', nargs='+', type=int, choices=range(1, 13))
    parser.add_argument('--base-url')
    parser.add_argument('--user', default='musel')
    parser.add_argument('--faults', action='store_true', help='Also submit every deliberate fault')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.command == 'live' and not args.base_url:
        parser.error('live needs --base-url')
    specs = load_specs(args.only)
    records = []
    for spec in specs:
        if args.command == 'build':
            record = build_problem(spec)
        elif args.command == 'verify':
            record = verify(spec)
        else:
            record = check_live(spec, args.base_url, args.user, args.faults)
        records.append(record)
        print(f"PASS {record['id']} ({record['cases']} tests)", flush=True)
    if args.command == 'build' and not args.only:
        course = ROOT / 'cojudge/courses' / COURSE_ID
        course.mkdir(parents=True, exist_ok=True)
        write_json(course / 'courseinfo.json', course_info(specs))
    if args.report:
        args.report.write_text(json.dumps(records, indent=2) + '\n')
    print(f"{len(records)} exercises; {sum(record['cases'] for record in records)} test cases.")


if __name__ == '__main__':
    main()
