"""Run real pytest once in a fresh process and return one verdict per test."""
from cojudge.pybites.runner import MARKER

SENTINEL = '# === SUPPLIED SQLMODEL TESTS ==='

RUNNER = r'''

import json as _json
from pathlib import Path as _Path
import os as _os
import subprocess as _subprocess
import sys as _sys
import tempfile as _tempfile
import xml.etree.ElementTree as _xml

_SM_RESULTS = None


def _sm_run_tests():
    source = _Path(__file__).read_text().split('# === SUPPLIED SQLMODEL TESTS ===', 1)[0]
    with _tempfile.TemporaryDirectory(prefix='sqlmodel-tests-') as folder:
        work = _Path(folder)
        (work / 'workout_app.py').write_text(source)
        (work / 'test_workout.py').write_text(_SM_TESTS)
        report = work / 'results.xml'
        env = dict(_os.environ)
        for key in ('PYTEST_ADDOPTS', 'PYTEST_PLUGINS', 'PYTHONPATH'):
            env.pop(key, None)
        env['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
        try:
            done = _subprocess.run(
                [_sys.executable, '-m', 'pytest', '-c', '/dev/null', '-p', 'no:cacheprovider',
                 '-q', '--tb=short', '--junitxml=' + str(report), str(work / 'test_workout.py')],
                cwd=work, env=env, capture_output=True, text=True, timeout=20)
            if report.exists():
                results = {}
                for case in _xml.parse(report).iter('testcase'):
                    name = case.get('name')
                    failures = [child for child in case if child.tag in ('failure', 'error', 'skipped')]
                    results[name] = ('FAILED ' + name + ' | ' +
                                     (failures[0].text or failures[0].get('message', 'test did not pass'))[-1800:]
                                     if failures else 'passed')
                if set(results) == set(_SM_IDS) and done.returncode in (0, 1):
                    return {key: value.replace('\n', ' | ') for key, value in results.items()}
            error = (done.stdout + done.stderr)[-2200:].replace('\n', ' | ')
        except _subprocess.TimeoutExpired:
            error = 'pytest exceeded 20 seconds'
        except Exception as exc:
            error = str(exc).replace('\n', ' | ')
        return {name: 'FAILED ' + name + ' | ' + error for name in _SM_IDS}


class Solution:
    def run(self, payload: str) -> str:
        global _SM_RESULTS
        target = _json.loads(payload)['test']
        if target == '--list':
            return _json.dumps(_SM_IDS)
        if target not in _SM_IDS:
            return 'Unknown test: ' + str(target)
        if _SM_RESULTS is None:
            _SM_RESULTS = _sm_run_tests()
        return _SM_RESULTS[target]
'''
