# Pybites SQLModel Path

[Open the course](https://cojudge.musel.dev/?course=pybites-sqlmodel).

The ten exercises follow the [SQLModel learning path](https://pybitesplatform.com/bites/paths/sqlmodel/)
in its original order. The public descriptions were read through the signed-in
browser on October 28, 2026. All ten original templates and test suites require
Pybites premium. This course uses recreated templates and tests. Each statement
identifies its source. The explicit exercise contract defines this version.

The course uses real SQLModel, SQLAlchemy, Pydantic, SQLite, FastAPI, HTTPX, and
pytest. It does not emulate these libraries. Later exercises supply the earlier
models and routes. A learner implements the new behavior at the top of the editor.

`runner.py` copies the learner implementation and supplied tests into a temporary
directory. It runs pytest once in a separate Python process. It reads each test's
verdict from JUnit XML. It caches the results for that submission. A missing test,
collection error, skipped test, or timeout cannot pass. Database fixtures create
and dispose a fresh engine for each test. API tests use SQLite `StaticPool` and
FastAPI `TestClient`, without network requests.

The test patterns follow the [official SQLModel testing guide](https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/).

## Authoring and checks

The nested uv project keeps its own Python 3.11 environment and lock file.

```sh
uv sync --project cojudge/sqlmodel_path --frozen
uv run python scripts/sqlmodel_course.py verify
uv run python scripts/sqlmodel_course.py build
uv run pytest tests/test_sqlmodel_course.py -q
```

Verification requires each reference to pass all tests. It requires each starter
to fail. It also checks at least two faulty implementations for each exercise. Generated
content uses IDs `pbs-01-*` through `pbs-10-*` and course ID `pybites-sqlmodel`.
The scripts write verification reports beside the source files.

## Runtime and deployment

The deployed application initially has a fixed Python image name, `python:3.11-slim`.
CoJudge commit `8b49b46` adds the `COJUDGE_PYTHON_IMAGE` setting. When that version
is deployed, select `cojudge/python-sqlmodel:2026-10-28` through that setting.
The runtime also includes the FastAPI course's authentication and HTML packages,
so both courses can use one image. FastAPI is pinned to the other course's 0.161.1 version.
Build the course runtime on the ARM VPS:

```sh
docker build -t cojudge/python-sqlmodel:2026-10-28 cojudge/sqlmodel_path
```

Its Dockerfile uses the stock Python image digest from that VPS. It installs the
locked packages with uv. Its PATH selects the installed virtual environment.
Preserve the stock image under a separate tag before changing the application tag:

```sh
docker tag python:3.11-slim cojudge/python-stock:pre-sqlmodel-2026-10-28
docker tag cojudge/python-sqlmodel:2026-10-28 python:3.11-slim
```

This changes the runtime for new Python execution containers, including other
courses. The Python version stays 3.11. Existing execution containers keep their
old image until the application removes them after its idle timeout. Do not stop
active executions. Verify the course only after the old pool has expired.
An explicit pull of the stock `python:3.11-slim` image replaces this local tag.
Reapply the course tag after such a pull. The separate course image remains saved.

Publish only `cojudge/problems/pbs-*` and `cojudge/courses/pybites-sqlmodel` to the
existing `cojudge-trial-data` volume. Do not copy or change progress directories.
No application restart is required for content publication.

```sh
ssh -N -L 15379:127.0.0.1:5379 my-vps
uv run python scripts/sqlmodel_course.py live --base-url http://127.0.0.1:15379
```

Live checks submit references and starters through the judge API. They do not
write learner progress. Roll back the runtime with:

```sh
docker tag cojudge/python-stock:pre-sqlmodel-2026-10-28 python:3.11-slim
```

Allow existing course execution containers to expire after rollback. Restore only
this course's content from its deployment backup when content rollback is needed.
