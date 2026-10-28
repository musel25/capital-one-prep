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
SQLModel is also installed to preserve the existing SQLModel course in the shared runtime.
Publish only `problems/pbf-*` and `courses/pybites-fastapi` into the content volume.
Keep the existing learner progress and other courses.

## Publication — October 28, 2026

The course is published with all 10 exercises and 59 checks. Local verification
passes every reference, rejects all starters, and detects all 12 supplied faults.
All 59 checks pass on the separate VPS judge. Its starters are rejected.
The final JWT run used fresh execution containers because other judge instances
can remove pooled containers from a different session. The production checks
pass both hello-world tests, token creation, an authenticated write, and rejection
of an ownership transfer. The public browser shows the course and 0 / 10 progress.
The repository test run passes 146 tests. The Cojudge image setting passes
264 unit tests and a production build. The CLI Run check passes both hello-world tests.

The production application remains `cojudge:typer-b58c197`. It now sets
`COJUDGE_PYTHON_IMAGE=cojudge-python:fastapi-20261028`.
The runtime image ID is `sha256:c2a1e4e43f2d24fe34ab7912e54364c30c0c270e544d787956ca1bc2e427d966`.
The previous application container is retained, stopped, as
`cojudge-profiles-pre-fastapi-20261028T123728`. The private configuration and
progress backup is `/home/ubuntu/cojudge-backups/fastapi-20261028.y1dFbs/`.
The startup health request needs the internal `X-CoJudge-User` header and retries
connection resets while the server starts. The first two attempts rolled back
before the corrected health request passed.

Only `pbf-*` definitions and the `pybites-fastapi` index were copied into the live
content volume. API checks do not mark exercises solved or change saved code.
The temporary judge instance was removed. The locked runtime also passed an
offline SQLModel/SQLite smoke check.
