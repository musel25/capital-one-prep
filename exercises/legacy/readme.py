from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


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

