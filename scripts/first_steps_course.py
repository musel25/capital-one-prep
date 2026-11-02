"""Build, verify, and check the Python First Steps beginner course on the real judge."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import ROOT, write_json
from cojudge.first_steps.support import COURSE_ID, build_problem, course_info, numbered, problem_id, verify
from scripts.pybites_course import submit


def check_live(number, spec, base_url, user):
    """The reference passes every test on the real judge. The starter and every fault fail."""
    pid = problem_id(number, spec)
    total = len(spec['tests'])
    good = submit(base_url, user, pid, spec['reference'])
    assert good.get('accepted') and good.get('totalTc') == total, f'{pid} reference: {str(good)[:1500]}'
    for name, code in [('starter', spec['starter'])] + [
            (fault, spec['reference'].replace(old, new, 1)) for fault, old, new in spec['faults']]:
        bad = submit(base_url, user, pid, code)
        assert bad.get('accepted') is False and bad.get('totalTc') == total, f'{pid} {name}: {str(bad)[:1000]}'
        assert any(row.get('isCorrect') is False for row in bad.get('results', [])), f'{pid} {name}: no failed test'
    return {'id': pid, 'cases': total, 'faults_rejected': len(spec['faults'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify', 'live'])
    parser.add_argument('--only', nargs='+', type=int)
    parser.add_argument('--base-url', help='live: an authorized tunnel to the judge, e.g. http://127.0.0.1:15381')
    parser.add_argument('--user', default='musel')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.command == 'live' and not args.base_url:
        parser.error('live needs --base-url')
    records = []
    for number, spec in numbered():
        if args.only and number not in args.only:
            continue
        if args.command == 'build':
            record = build_problem(number, spec)
        elif args.command == 'verify':
            record = verify(number, spec)
        else:
            record = check_live(number, spec, args.base_url, args.user)
        record.pop('outputs', None)
        records.append(record)
        print(f"PASS {record['id']} ({record['cases']} tests)", flush=True)
    if args.command == 'build' and not args.only:
        folder = ROOT / 'cojudge/courses' / COURSE_ID
        folder.mkdir(parents=True, exist_ok=True)
        write_json(folder / 'courseinfo.json', course_info())
    if args.report:
        args.report.write_text(json.dumps(records, indent=2) + '\n')
    print(f"{len(records)} exercises; {sum(r['cases'] for r in records)} test cases.")


if __name__ == '__main__':
    main()
