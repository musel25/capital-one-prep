"""Run one external contract against a sandbox copy of learner code."""
import json
import sys
from pathlib import Path

from contracts import CHECKS
revision = int(sys.argv[3]) if len(sys.argv) > 3 else 1
if revision == 2:
    from early import CHECKS as early
    from middle import CHECKS as middle
    from late import CHECKS as late
    CHECKS = {**CHECKS, **early, **middle, **late}
sys.path.insert(0, str(Path(sys.argv[2]).resolve()))

try:
    CHECKS[sys.argv[1]]()
except AssertionError as error:
    print(json.dumps({'status': 'failed', 'detail': str(error) or 'A required behavior assertion failed.'}))
    raise SystemExit(1)
except Exception as error:
    print(json.dumps({'status': 'error', 'detail': f'{type(error).__name__}: {error}'}))
    raise SystemExit(2)
else:
    print(json.dumps({'status': 'passed', 'detail': 'All external checks for this task passed.'}))
