"""Build, verify, or check the Typer learning path on the live judge."""
import argparse
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from cojudge.typer_path.support import build, full_source, load_specs, verify
from scripts.pybites_course import request_json, submit


def check_samples(base_url, user, spec):
    metadata = json.loads((Path(__file__).resolve().parents[1] / 'cojudge/problems' /
                           spec['id'] / 'metadata.json').read_text())
    job = request_json(base_url, '/api/run', user, {
        'problemId': spec['id'], 'language': 'python',
        'code': full_source(spec, spec['reference']), 'testCases': metadata['testCases'],
    })
    assert 'jobId' in job, job
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        result = request_json(base_url, '/api/run?jobId=' + job['jobId'], user)
        if result.get('ready'):
            assert len(result.get('results', [])) == 3 and all(
                case['isCorrect'] for case in result['results']), (spec['id'], result)
            return
        time.sleep(0.25)
    raise TimeoutError(job['jobId'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify', 'live'])
    parser.add_argument('--base-url')
    parser.add_argument('--user', default='musel')
    args = parser.parse_args()
    if args.command == 'live' and not args.base_url:
        parser.error('live requires --base-url')
    if args.command == 'build':
        results = build()
    else:
        results = []
        for spec in load_specs():
            if args.command == 'verify':
                result = verify(spec)
            else:
                good = submit(args.base_url, args.user, spec['id'], full_source(spec, spec['reference']))
                assert good.get('accepted'), (spec['id'], good)
                assert good.get('totalTc') == len(json.loads(
                    (Path(__file__).resolve().parents[1] / 'cojudge/problems' /
                     spec['id'] / 'official-tests.json').read_text()))
                bad = submit(args.base_url, args.user, spec['id'], full_source(spec, spec['template']))
                assert not bad.get('accepted') and not bad.get('error'), (spec['id'], bad)
                check_samples(args.base_url, args.user, spec)
                result = {'id': spec['id'], 'reference': 'accepted', 'template': 'rejected', 'samples': 'passed'}
            results.append(result)
            print(result, flush=True)
    print(f'{len(results)} exercises passed.', flush=True)


if __name__ == '__main__':
    main()
