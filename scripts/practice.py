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
from exercises.catalog import BY_ID, TASKS, LEGACY_BY_ID, LEGACY_TASKS, public_tasks
from exercises.coach.starters import apply_starter
from exercises.legacy.readme import readme as legacy_readme

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


def clarifications(task):
    return f'''# Interviewer clarification sheet — {task.id}

Use this after writing your questions. In a mock, the interviewer can read this
file and answer your questions one at a time. These are acceptance criteria,
not a diagnosis or a suggested implementation.

## Required behavior

{task.contract}

## Example request

```sh
{task.probe}
```

## Scope

All data is fictional and local. One server process and sequential requests are
in scope; persistence, authentication and distributed concurrency are not.
Preserve fixtures and existing supported behavior. Ask about ambiguous policy;
record any assumption the contract does not resolve rather than inventing one.
'''


def readme(task, destination, *, mode='interview'):
    requirements = (f"## Required contract\n\n{task.contract}\n\nExample request:\n\n```sh\n{task.probe}\n```\n"
                    if mode == 'guided' else
                    "## Clarify before coding\n\nWrite your questions and assumptions first. Then open `CLARIFICATIONS.md` "
                    "for the interviewer's acceptance criteria, or ask your mock interviewer "
                    "to read it and answer only the questions you ask. That file contains "
                    "requirements, not the solution. Read it before final verification.\n")
    return f'''# {task.id}: {task.title}

## Interview prompt

{task.brief}

## Product context

{task.orientation}

{requirements}
## Work through the problem

1. Explore the public interface and relevant code. State a hypothesis (or feature
   design) and a small experiment that could disprove it.
2. Describe a test's input, expected response and expected state in your own
   words. You may ask AI to implement that test. Review it and run it **before**
   changing application code; explain why it fails.
3. Make or delegate the smallest change. Inspect the diff, run the tests, and
   ask for additional boundaries only after your first regression is covered.
4. Explain the cause, user impact, evidence, and one remaining limitation in English.

Use 20 minutes for the task and 5 for the explanation. Record incomplete work
honestly. For guided practice, use `start {task.id} --mode guided` to create a
separate attempt with acceptance criteria visible from the start.

## Run locally

From this attempt folder:

```sh
cd "{destination}"
test -d .venv || uv venv
uv sync
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs . If port 8000 is busy,
use 8001 and update your URLs. Reloading resets in-memory data. `app/main.py`
is the entry point; discover the remaining structure rather than assuming it
matches another exercise. The browser UI is context unless your task says otherwise.

In another terminal, from this folder:

```sh
uv run pytest
```

Public tests protect startup and supplied behavior where present. Passing them
alone does not solve the assigned task. Extend `tests/` with real requests using
`TestClient(create_app())` for fresh state. Never change fixtures to satisfy a test.

## Check and record evidence

After implementing and reviewing the acceptance criteria:

```sh
uv run --project "{ROOT}" python "{ROOT / 'scripts/practice.py'}" check "{destination}"
```

The checker runs a temporary copy. It never resets or edits this attempt.
Exit 0 means sampled checks passed; 1 means an unmet assertion; 2 means a setup
or execution error. A pass is not proof of general correctness or interview
readiness. Keep `.practice.json`: it selects this exercise's original checker.

Save `NOTES.md` with your questions, hypothesis, reproduction, test predictions,
commands/results, explanation of the change, AI help used and remaining uncertainty.
Keep your code and tests here. The planner cannot observe local checks; record
completion yourself. Do not copy a prior solution into a new exercise.

This is an original constructed training application with one seeded defect or
missing feature. It is not an employer question or a claim about an upstream
framework. Instructor source remains outside this folder; avoid opening it
before an independent attempt. No credentials or banking access are required.
'''


def build(task_id: str, destination: Path, *, reference=False, revision=2, mode='interview'):
    if revision not in (1, 2) or mode not in ('interview', 'guided'):
        raise ValueError('Unsupported exercise revision or mode')
    task = (LEGACY_BY_ID if revision == 1 else BY_ID)[task_id]
    shutil.copytree(ROOT / 'exercises/templates' / task.context, destination, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', *(['tests'] if revision == 1 else [])))
    (destination / 'app/__init__.py').write_text('')
    (destination / 'app/static/style.css').write_text(CSS)
    (destination / 'tests').mkdir(exist_ok=True)
    (destination / 'tests/test_smoke.py').write_text(SMOKE)
    for name in ('pyproject.toml', 'uv.lock'):
        shutil.copy2(ROOT / name, destination / name)
    marker = ({'schema_version': 1, 'task_id': task_id} if revision == 1 else
              {'schema_version': 2, 'task_id': task_id, 'catalog_revision': 2, 'mode': mode})
    (destination / '.practice.json').write_text(json.dumps(marker, indent=2) + '\n')
    if revision == 1:
        (destination / 'README.md').write_text(legacy_readme(task, destination))
    else:
        (destination / 'README.md').write_text(readme(task, destination, mode=mode))
        (destination / 'CLARIFICATIONS.md').write_text(clarifications(task))
    if not reference:
        apply_starter(task_id, destination, revision=revision)


def start(task_id: str, output_root: Path, *, mode='interview') -> Path:
    if task_id not in BY_ID:
        raise ValueError(f'Unknown task: {task_id!r}. Run list for valid IDs.')
    output_root = output_root.expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    # Atomic mkdir and random suffix prevent same-instant or concurrent starts
    # from selecting an existing attempt. There is no overwrite/reset command.
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    destination = output_root / f'{task_id}-{stamp}-{uuid.uuid4().hex[:8]}'
    destination.mkdir(exist_ok=False)
    build(task_id, destination, mode=mode)
    return destination


def manifest(path: Path) -> tuple[str, int]:
    marker = path / '.practice.json'
    if not marker.is_file() or marker.is_symlink():
        raise ValueError('Attempt manifest .practice.json is missing or unsafe; use start TASK_ID first.')
    try:
        data = json.loads(marker.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f'Invalid attempt manifest: {error}') from error
    if (not isinstance(data, dict) or type(data.get('schema_version')) is not int
            or data['schema_version'] not in (1, 2)
            or not isinstance(data.get('task_id'), str)):
        raise ValueError('Unknown schema or task in attempt manifest.')
    revision = 1 if data['schema_version'] == 1 else data.get('catalog_revision')
    if type(revision) is not int or revision not in (1, 2) or revision != data['schema_version']:
        raise ValueError('Unsupported catalog revision in attempt manifest.')
    catalog = LEGACY_BY_ID if revision == 1 else BY_ID
    if data['task_id'] not in catalog:
        raise ValueError('Unknown task in attempt manifest.')
    return data['task_id'], revision


def check(path: Path) -> dict:
    path = path.expanduser().resolve()
    task_id, revision = manifest(path)
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
            result = subprocess.run([sys.executable, str(ROOT / 'exercises/coach/run.py'), task_id, str(copy), str(revision)],
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


def verify(*, revision=2) -> list[dict]:
    report = []
    with tempfile.TemporaryDirectory(prefix='capital-one-verify-') as temporary:
        for task in LEGACY_TASKS if revision == 1 else TASKS:
            outcomes = {}
            for version in ('starter', 'reference'):
                destination = Path(temporary) / f'{task.id}-{version}'
                build(task.id, destination, reference=version == 'reference', revision=revision)
                outcomes[version] = check(destination)
                public = subprocess.run([sys.executable, '-m', 'pytest', '-q'], cwd=destination,
                                        capture_output=True, text=True, timeout=40,
                                        env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
                outcomes[f'public_{version}'] = {'passed': public.returncode == 0,
                                               'output': public.stdout[-2500:] + public.stderr[-1000:]}
            report.append({'task_id': task.id, 'starter_fails': outcomes['starter']['status'] == 'failed',
                           'reference_passes': outcomes['reference']['status'] == 'passed',
                           'public_starter_passes': outcomes['public_starter']['passed'],
                           'public_reference_passes': outcomes['public_reference']['passed'], 'evidence': outcomes})
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
    starting.add_argument('--mode', choices=('interview', 'guided'), default='interview',
                          help='Interview: questions before contract; guided: show contract immediately')
    checking = sub.add_parser('check', help='Execute external coach checks on a temporary copy')
    checking.add_argument('attempt', type=Path)
    checking.add_argument('--json', action='store_true')
    verifying = sub.add_parser('verify', help='Maintainer: verify all faulty starters and working references')
    verifying.add_argument('--json', action='store_true')
    verifying.add_argument('--revision', type=int, choices=(1, 2), default=2)
    args = parser.parse_args()
    try:
        if args.command == 'list':
            print(json.dumps(public_tasks(), indent=2) if args.json else '\n'.join(f'{task.id:13} {task.title}' for task in TASKS))
        elif args.command == 'start':
            path = start(args.task_id, args.output_root, mode=args.mode)
            print(json.dumps({'task_id': args.task_id, 'path': str(path)}) if args.json else f'Created: {path}\nRead {path / "README.md"}\nYour work will never be overwritten by start.')
        elif args.command == 'check':
            result = check(args.attempt)
            print(json.dumps(result, indent=2) if args.json else f'{result["task_id"]}: {result["status"].upper()} — {result["detail"]}\nExecuted real checks on a temporary copy. Original attempt preserved. This is sampled verification, not a readiness score.')
            return result['exit_code']
        else:
            result = verify(revision=args.revision)
            print(json.dumps(result, indent=2) if args.json else '\n'.join(f'{row["task_id"]}: starter {"EXPECTED FAILURE" if row["starter_fails"] else "INVALID"}; reference {"PASS" if row["reference_passes"] else "FAIL"}; public tests {"PASS" if row["public_starter_passes"] and row["public_reference_passes"] else "FAIL"}' for row in result))
            return 0 if all(row['starter_fails'] and row['reference_passes'] and row['public_starter_passes']
                            and row['public_reference_passes'] for row in result) else 1
    except (ValueError, OSError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
