#!/usr/bin/env python3
"""Create preserved practice attempts and verify copies against coach contracts."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from exercises.catalog import BY_ID, TASKS, public_tasks
from exercises.coach.starters import apply_starter

IGNORED = {'.venv', '.git', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', 'node_modules'}
CSS = '''body{font:16px/1.5 system-ui,sans-serif;background:#f6f8fc;color:#19273b;margin:0}main{max-width:850px;margin:3rem auto;padding:2rem;background:white;border:1px solid #dae2ef;border-radius:12px}h1{margin-top:0}form{display:flex;gap:1rem;flex-wrap:wrap;align-items:end}label{display:flex;flex-direction:column;gap:.3rem}input,select,button{font:inherit;padding:.5rem;border:1px solid #cad4e4;border-radius:5px}button{background:#375dcc;color:white;cursor:pointer}pre{background:#edf1f8;white-space:pre-wrap;overflow-wrap:anywhere;padding:1rem}a{color:#375dcc}@media(max-width:650px){main{margin:0;padding:1rem;border:0}}
'''
SMOKE = '''"""Public startup tests; add your regression and boundary tests here."""
from fastapi.testclient import TestClient
from app.main import create_app


def test_local_application_boots_and_serves_ui():
    client = TestClient(create_app())
    assert client.get('/health').json() == {'status': 'ok'}
    assert client.get('/').status_code == 200
    assert client.get('/static/app.js').status_code == 200
    assert client.get('/static/style.css').status_code == 200


def test_api_documentation_is_available():
    client = TestClient(create_app())
    assert client.get('/openapi.json').status_code == 200
'''


def readme(task, destination):
    coaching = ('Guiado: primero describe una hipótesis, reproduce, escribe una prueba y después edita. Puedes pedir una pista.'
                if task.id <= 'd03-feature' else
                'Práctica independiente: 20 minutos de implementación y después 5 minutos de explicación. Registra ayuda recibida. Para la segunda tarea crea una copia nueva.')
    context = {
        'bank': 'Cedar Wallet. Checking starts at 100000 cents; savings at 20000. Seven transactions include mixed timezone offsets, equal instants, posted/pending purchases and a 499-cent refund linked to a 1999-cent purchase. Inspect app/store.py for the full fictitious fixture, without editing it to satisfy a test.',
        'settlements': 'Fern Merchant Operations. Six fictitious charges cover captured, authorized, refunded, already-settled and another merchant. Gross amounts and fees are integer cents. Inspect app/store.py for the complete fixture.',
        'promotions': 'Juniper Rewards. Fictitious UTC promotion runs from October 30 to November 1, 2026; membership and minimum spend apply. The browser allows custom purchases. No database or real rewards account exists.',
        'inventory': 'Harbor Supply. dock starts with 5 units at 4000 cents; cable starts with 10 units at 1200 cents. Reservation IDs are allocated locally. Inspect app/store.py for the complete fixture.',
    }[task.context]
    return f'''# {task.id}: {task.title}

{coaching}

## Interview prompt (English)

{task.brief}

## Required contract

{task.contract}

## Context and fixtures

{context}

Each task is an independent snapshot. It contains one deliberately seeded defect or missing feature. Other functionality is supplied as context, not as extra assigned work. These are original constructed exercises; the bugs are not claims about FastAPI, Capital One, or an upstream template. Everything is fictional and local. No credentials or banking access are needed.

Repository orientation: `app/main.py` registers HTTP routes; the other Python modules hold models, state and business behavior; `app/static/` contains the small browser interface; `tests/` is yours to extend. Read the application to locate the relevant behavior: this brief deliberately does not identify the defective line.

## Run locally

From this attempt folder (not the repository root):

```sh
cd "{destination}"
test -d .venv || uv venv
uv sync
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs . If that port is occupied use `--port 8001` and update URLs. Restarting or reloading resets in-memory data. One server worker is the scope; production persistence, authentication and distributed concurrency are out of scope.

In a second terminal:

```sh
cd "{destination}"
uv run pytest
{task.probe}
```

The included tests prove startup only; passing them does not solve the exercise. Add your own tests using `TestClient(create_app())` for fresh state per test. Make assertions about API responses and resulting state, including rejected inputs.

After your attempt, run the external coach check from this folder:

```sh
uv run --project "{ROOT}" python "{ROOT / 'scripts/practice.py'}" check "{destination}"
```

The checker executes the real code from a temporary copy and does not reset or edit your workspace. It returns 0 for passed checks, 1 for an unmet behavior assertion, and 2 for execution/setup errors. A check pass is evidence only for the sampled contract, not proof of interview readiness. Record the output, tests you added, and remaining uncertainty. Instructor tests and reference code are not copied here; avoid opening repository instructor material before the independent attempt.

## Deliverables and explanation

1. Leave your edited code and regression tests in this folder; never edit fixtures to disguise the failure.
2. Save `NOTES.md` with the symptom, hypothesis, reproduction, root cause or design, commands/results, boundaries tested, and whether you used help.
3. Explain the user impact, the smallest change, why your test would fail before it, and one remaining limitation. Use English for the five-minute explanation.

Evaluate: correct happy path; boundary/rejection behavior; no unrelated regressions; understandable small change; explanation grounded in an observed test. Stopping at the time limit is valid: record incomplete work honestly. The planner uses self-reported completion and cannot observe these commands.
'''


def build(task_id: str, destination: Path, *, reference=False):
    task = BY_ID[task_id]
    shutil.copytree(ROOT / 'exercises/templates' / task.context, destination, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    (destination / 'app/__init__.py').write_text('')
    (destination / 'app/static/style.css').write_text(CSS)
    (destination / 'tests').mkdir(exist_ok=True)
    (destination / 'tests/test_smoke.py').write_text(SMOKE)
    for name in ('pyproject.toml', 'uv.lock'):
        shutil.copy2(ROOT / name, destination / name)
    (destination / '.practice.json').write_text(json.dumps({'schema_version': 1, 'task_id': task_id}, indent=2) + '\n')
    (destination / 'README.md').write_text(readme(task, destination))
    if not reference:
        apply_starter(task_id, destination)


def start(task_id: str, output_root: Path) -> Path:
    if task_id not in BY_ID:
        raise ValueError(f'Unknown task: {task_id!r}. Run list for valid IDs.')
    output_root = output_root.expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    # Atomic mkdir and random suffix prevent same-instant or concurrent starts
    # from selecting an existing attempt. There is no overwrite/reset command.
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    destination = output_root / f'{task_id}-{stamp}-{uuid.uuid4().hex[:8]}'
    destination.mkdir(exist_ok=False)
    build(task_id, destination)
    return destination


def manifest(path: Path) -> str:
    marker = path / '.practice.json'
    if not marker.is_file() or marker.is_symlink():
        raise ValueError('Attempt manifest .practice.json is missing or unsafe; use start TASK_ID first.')
    try:
        data = json.loads(marker.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f'Invalid attempt manifest: {error}') from error
    if (not isinstance(data, dict) or data.get('schema_version') != 1
            or not isinstance(data.get('task_id'), str) or data['task_id'] not in BY_ID):
        raise ValueError('Unknown schema or task in attempt manifest.')
    return data['task_id']


def check(path: Path) -> dict:
    path = path.expanduser().resolve()
    task_id = manifest(path)
    # Do not follow project symlinks into unrelated user files. Environment/cache
    # directories are skipped entirely, including their normal interpreter links.
    for directory, dirs, files in os.walk(path, followlinks=False):
        dirs[:] = [name for name in dirs if name not in IGNORED]
        for name in dirs + files:
            if (Path(directory) / name).is_symlink():
                raise ValueError('Attempt contains a symlink outside ignored environments/caches; check refused.')
    with tempfile.TemporaryDirectory(prefix='capital-one-check-') as temporary:
        copy = Path(temporary) / 'attempt'
        shutil.copytree(path, copy, ignore=lambda _, names: set(names) & IGNORED)
        environment = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
        try:
            result = subprocess.run([sys.executable, str(ROOT / 'exercises/coach/run.py'), task_id, str(copy)],
                                    cwd=temporary, env=environment, capture_output=True, text=True, timeout=40)
        except subprocess.TimeoutExpired:
            return {'task_id': task_id, 'status': 'error', 'detail': 'Verification exceeded 40 seconds.', 'exit_code': 2}
        try:
            outcome = json.loads(result.stdout.strip().splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            outcome = {'status': 'error', 'detail': f'Coach runner could not execute. {result.stderr[-1500:]}'}
        if result.returncode not in (0, 1, 2) or outcome.get('status') not in ('passed', 'failed', 'error'):
            outcome = {'status': 'error', 'detail': 'Unexpected coach runner result.'}
        outcome.update(task_id=task_id, exit_code={'passed': 0, 'failed': 1, 'error': 2}[outcome['status']])
        return outcome


def verify() -> list[dict]:
    report = []
    with tempfile.TemporaryDirectory(prefix='capital-one-verify-') as temporary:
        for task in TASKS:
            outcomes = {}
            for version in ('starter', 'reference'):
                destination = Path(temporary) / f'{task.id}-{version}'
                build(task.id, destination, reference=version == 'reference')
                outcomes[version] = check(destination)
            report.append({'task_id': task.id, 'starter_fails': outcomes['starter']['status'] == 'failed',
                           'reference_passes': outcomes['reference']['status'] == 'passed', 'evidence': outcomes})
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    listing = sub.add_parser('list', help='Show the twenty independent exercises')
    listing.add_argument('--json', action='store_true')
    starting = sub.add_parser('start', help='Create a unique learner-only attempt; never overwrites')
    starting.add_argument('task_id')
    starting.add_argument('--output-root', type=Path, default=ROOT / 'attempts', help='Defaults to ignored attempts/; custom locations are not automatically Git-ignored')
    starting.add_argument('--json', action='store_true')
    checking = sub.add_parser('check', help='Execute external coach checks on a temporary copy')
    checking.add_argument('attempt', type=Path)
    checking.add_argument('--json', action='store_true')
    verifying = sub.add_parser('verify', help='Maintainer: verify all faulty starters and working references')
    verifying.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'list':
            print(json.dumps(public_tasks(), indent=2) if args.json else '\n'.join(f'{task.id:13} {task.title}' for task in TASKS))
        elif args.command == 'start':
            path = start(args.task_id, args.output_root)
            print(json.dumps({'task_id': args.task_id, 'path': str(path)}) if args.json else f'Created: {path}\nRead {path / "README.md"}\nYour work will never be overwritten by start.')
        elif args.command == 'check':
            result = check(args.attempt)
            print(json.dumps(result, indent=2) if args.json else f'{result["task_id"]}: {result["status"].upper()} — {result["detail"]}\nExecuted real checks on a temporary copy. Original attempt preserved. This is sampled verification, not a readiness score.')
            return result['exit_code']
        else:
            result = verify()
            print(json.dumps(result, indent=2) if args.json else '\n'.join(f'{row["task_id"]}: starter {"EXPECTED FAILURE" if row["starter_fails"] else "INVALID"}; reference {"PASS" if row["reference_passes"] else "FAIL"}' for row in result))
            return 0 if all(row['starter_fails'] and row['reference_passes'] for row in result) else 1
    except (ValueError, OSError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
