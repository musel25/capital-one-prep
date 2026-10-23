"""Run one external contract against a sandbox copy of learner code."""
import json
import sys
from pathlib import Path

from contracts import CHECKS
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
