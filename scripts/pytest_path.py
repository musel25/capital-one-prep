"""Build, verify, or check the Pytest learning path on a live CoJudge server."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.pytest_path.support import build, checks, full_source, load_specs, verify
from scripts.pybites_course import submit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify', 'live'])
    parser.add_argument('--base-url')
    parser.add_argument('--user', default='musel')
    args = parser.parse_args()
    if args.command == 'live' and not args.base_url:
        parser.error('live requires --base-url')
    if args.command == 'build':
        records = build()
    else:
        records = []
        for spec in load_specs():
            if args.command == 'verify':
                result = verify(spec)
            else:
                good = submit(args.base_url, args.user, spec['id'], full_source(spec, spec['reference']))
                assert good.get('accepted') and good.get('totalTc') == len(checks(spec)), (spec['id'], good)
                bad = submit(args.base_url, args.user, spec['id'], full_source(spec, spec['starter']))
                assert not bad.get('accepted') and not bad.get('error'), (spec['id'], bad)
                result = {'id': spec['id'], 'checks': len(checks(spec)), 'reference': 'accepted', 'starter': 'rejected'}
            records.append(result)
            print(result, flush=True)
    print(f'{len(records)} exercises passed.', flush=True)


if __name__ == '__main__':
    main()
