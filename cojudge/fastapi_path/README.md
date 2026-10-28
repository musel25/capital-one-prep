# Pybites FastAPI Path on Cojudge

[Open the course](https://cojudge.musel.dev/?course=pybites-fastapi).

All 10 exercises of the [Pybites FastAPI path](https://pybitesplatform.com/bites/paths/fastapi/), in source order.
The editor contains the imported template, tests, and a supplied adapter.
The adapter runs real pytest, FastAPI, and HTTPX. It does not emulate these packages.
Each test runs in a fresh process. Submit gives each test its own execution budget.

## Source and adaptations

`source-pages.json` records the exercise pages accessible in the user's signed-in session.
All 10 pages exposed their starter and tests. The export redacted example password
fields, token assignments, and the example signing key. The builder restores the
types and assignments. It uses the supplied `LAME_PASSWORD = "1234"` test value
and an explicit classroom signing key. These are exercise values, not account credentials.

The source templates use a datetime evaluated at import time. The builder changes
this to `Field(default_factory=datetime.now)`. Each FoodEntry gets its own timestamp.
`test_added_` functions add checks for timestamps, per-user calorie limits, atomic
rejections, escaped HTML, JWT validation, and ownership. The reference solutions
are authored for this course. JWT expiry uses UTC.

The early retrieve exercise deliberately preserves the source tests' KeyError for
a missing read. Later exercises introduce HTTPException. The body/path IDs match
in the update exercises. The fixed signing key, in-memory stores, and create_user
test endpoint belong to this classroom exercise.

## Build and checks

Run from the repository root:

```bash
uv run python scripts/fastapi_path.py verify
uv run python scripts/fastapi_path.py build
uv run pytest tests/test_fastapi_path.py
uv run python scripts/fastapi_path.py live --base-url http://127.0.0.1:15379
```

The verifier requires every reference test to pass. It rejects each starter.
It also checks that the tests detect each supplied faulty reference variant.
`live` tests each reference and starter through the actual judge API. It handles
the separate Submit batches. It does not update learner progress.

## Runtime

This folder is a separate uv project for Python 3.11. Its lock file pins all packages.
It does not change the preparation website's Python environment.

```bash
docker build -t cojudge-python:fastapi-20261028 cojudge/fastapi_path
```

Set `COJUDGE_PYTHON_IMAGE=cojudge-python:fastapi-20261028` when starting Cojudge.
The judge must include the custom Python image setting from commit `8b49b46`.
Dependencies are installed when building the image. Tests run without downloads.
Publish only `problems/pbf-*` and `courses/pybites-fastapi` into the content volume.
Keep the existing learner progress and other courses.
