"""Build, verify, or check the Pybites FastAPI course on the live judge."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.fastapi_path.support import build, full_source, load_specs, verify
from scripts.pybites_course import request_json
import time


def submit_all(base_url, spec, code):
    start = 0
    total = len(spec['test_ids'])
    while start < total:
        job = request_json(base_url, '/api/submit', 'musel', {
            'problemId': spec['id'], 'language': 'python', 'code': code, 'startTcNo': start})
        assert 'jobId' in job, job
        deadline = time.monotonic() + 180
        while True:
            result = request_json(base_url, '/api/submit?jobId=' + job['jobId'], 'musel')
            if result.get('ready'):
                break
            assert time.monotonic() < deadline, job
            time.sleep(0.25)
        if not result.get('accepted'):
            return result
        checked = len(result.get('results', []))
        assert checked > 0, result
        start += checked
    return {'accepted': True, 'totalTc': total}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify', 'live'])
    parser.add_argument('--only', nargs='+', type=int)
    parser.add_argument('--base-url')
    args = parser.parse_args()
    specs = load_specs(args.only)
    if args.command == 'build':
        assert not args.only, 'Build the complete course to preserve the course list'
        build(specs)
    for spec in specs:
        if args.command == 'verify':
            result = verify(spec)
            print(f"PASS {result['id']} ({result['cases']} tests, {len(result['faults'])} faults)", flush=True)
        elif args.command == 'live':
            assert args.base_url, '--base-url required'
            good = submit_all(args.base_url, spec, full_source(spec, spec['reference']))
            assert good.get('accepted') and good.get('totalTc') == len(spec['test_ids']), (spec['id'], good)
            bad = submit_all(args.base_url, spec, full_source(spec, spec['template']))
            assert not bad.get('accepted'), (spec['id'], bad)
            print(f"PASS {spec['id']} ({good['totalTc']} live tests; starter rejected)", flush=True)
        else:
            print(f"Built {spec['id']}")


if __name__ == '__main__':
    main()
