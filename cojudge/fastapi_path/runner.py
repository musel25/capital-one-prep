"""Adapter for real pytest and FastAPI inside the locked Python image."""

ADAPTER = r'''

class Solution:
    def run(self, payload: str) -> str:
        import json
        import os
        from pathlib import Path
        import subprocess
        import sys
        import tempfile

        test = json.loads(payload)['test']
        if test not in _FA_IDS:
            return 'Unknown test: ' + str(test)
        with tempfile.TemporaryDirectory(prefix='fastapi-bite-') as work:
            source = Path(__file__).read_text().split('# === SUPPLIED FASTAPI TESTS ===', 1)[0]
            Path(work, _FA_MODULE + '.py').write_text(source)
            Path(work, 'test_bite.py').write_text(_FA_TESTS)
            env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', PYTHONDONTWRITEBYTECODE='1')
            try:
                done = subprocess.run(
                    [sys.executable, '-m', 'pytest', '-q', '--tb=short', '--disable-warnings',
                     '-p', 'no:cacheprovider', 'test_bite.py::' + test],
                    cwd=work, env=env, capture_output=True, text=True, timeout=12)
            except subprocess.TimeoutExpired:
                return 'FAILED ' + test + ' | Test exceeded 12 seconds'
            if done.returncode == 0:
                return 'passed'
            output = done.stdout + done.stderr
            lines = [line.strip() for line in output.splitlines() if line.strip()]
            return ('FAILED ' + test + ' | ' + ' | '.join(lines))[:6000]
'''
