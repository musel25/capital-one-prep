"""Build and verify the 11-exercise Pybites Collections course."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.authoring.support import ROOT, write_json
from cojudge.collections_path.support import (
    COURSE_ID, build_problem, course_info, full_source, load_specs, problem_id, verify,
)
from cojudge.pybites.support import run_all
from scripts.pybites_course import submit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify', 'live'])
    parser.add_argument('--only', nargs='+', type=int, choices=range(1, 12))
    parser.add_argument('--base-url')
    parser.add_argument('--user', default='musel')
    args = parser.parse_args()
    if args.command == 'live' and not args.base_url:
        parser.error('live requires --base-url')
    specs = load_specs(args.only)
    records = []
    for spec in specs:
        if args.command == 'build':
            result = build_problem(spec)
        elif args.command == 'verify':
            result = verify(spec)
        else:
            pid = problem_id(spec)
            expected = len(run_all(spec, spec['reference']))
            good = submit(args.base_url, args.user, pid, full_source(spec, spec['reference']))
            assert good.get('accepted') and good.get('totalTc') == expected, f'{pid}: {str(good)[:1800]}'
            bad = submit(args.base_url, args.user, pid, full_source(spec, spec['template']))
            assert not bad.get('accepted'), f'{pid}: starter was accepted'
            result = {'id': pid, 'cases': expected}
        records.append(result)
        print(f"PASS {result['id']} ({result['cases']} tests)", flush=True)
    if args.command == 'build' and not args.only:
        course = ROOT / 'cojudge/courses' / COURSE_ID
        course.mkdir(parents=True, exist_ok=True)
        write_json(course / 'courseinfo.json', course_info(specs))
    print(f"{len(records)} exercises; {sum(r['cases'] for r in records)} test cases.")


if __name__ == '__main__':
    main()
