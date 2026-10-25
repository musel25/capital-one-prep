# Local practice system

Twenty original tasks and four larger mock tasks support the ten-day plan. These are original fictional exercises,
inspired by the familiar API/routes/models/UI structure of public FastAPI
applications. They do not reproduce an employer assessment or identify upstream
bugs. No real accounts, credentials, external API or banking access is involved.

```sh
test -d .venv || uv venv
uv sync
uv run python scripts/practice.py list
uv run python scripts/practice.py start d01-bug
```

Open the returned folder in your editor and read its README. It includes the
English interview prompt, product context, startup commands, public tests and
deliverables. In the default interview mode, write your questions first and then
open `CLARIFICATIONS.md` for the exact contract. A mock interviewer can read that
file and answer only the questions you ask. `--mode guided` includes the contract
in the README immediately. Both modes have the same task and checks.
`uv run uvicorn app.main:app --reload` runs its API
and browser UI. Save your code, tests and notes inside the returned attempt.

Create a fresh attempt for the feature task. Starting a task again creates a new
folder with a UTC timestamp and unique suffix; there is no reset/overwrite
operation. Default `attempts/` is Git-ignored. The optional `--output-root` is for
custom storage or platform tests; that location is not automatically ignored.

```sh
uv run python scripts/practice.py check attempts/<returned-folder>
```

`check` executes the real application against instructor checks in a temporary
copy, outside the learner workspace. It does not edit or reset learner files and
does not copy instructor code into them. Environments and caches are skipped;
other symlinks are rejected. It uses the repository's uv environment, so keep the
exercise within the supplied dependency set. This is a local training tool for
your own code, not a security sandbox for untrusted programs.

Exit codes: **0** sampled behavior passed; **1** an expected behavior assertion
failed; **2** invalid path, execution, import or setup error. A seeded starter is
expected to return 1. Passing is evidence for these checks only; it does not prove
general correctness or interview readiness. The web planner cannot observe the
CLI, so record completion and assistance honestly.

Among the original d01–d10 tasks, from d02-feature onward each task uses a distinct application, even within a day.
Different domain rules, data shapes and module responsibilities require fresh
navigation. Python/FastAPI and the run commands stay familiar. The initial Cedar
Wallet tasks remain available; no existing learner folder is migrated.

Days 8 and 10 now use **Support Ops** and **Parcel Dispatch**, two fuller
applications with UI, routes, validation, state, event history and multiple
service modules. Each mock pairs a bug and feature in the same product but in
independent snapshots: the feature starts with the bug already corrected.
Use `mock-support-bug` / `mock-support-feature` or
`mock-dispatch-bug` / `mock-dispatch-feature`. Keep each returned folder.
The old day-8/day-10 tasks remain available through the CLI and the website's
**Previous exercises** view.

New manifests select catalog revision 2. Older schema-1 manifests still select
their original contracts, even when a task ID now describes a different project.
Keep `.practice.json` with your attempt. The web planner preserves existing task
IDs, notes and timers; its updated brief applies to newly created attempts.

The public learner tests verify startup and existing behavior in the new projects.
They intentionally do not cover the assigned defect or feature. Describe and add
regression and boundary tests before claiming a fix. The external checks sample the published behavior; their failure
messages describe the contract without printing the hidden test source.

## Instructor and maintenance material

Day 7 uses a separate pure-Python progressive exercise:
`uv run python scripts/progressive.py start`. Open the returned folder and follow
its README through stages 1–3. One summarize function grows as requirements arrive;
earlier tests keep running. Use `uv run pytest -q` inside that attempt.
It does not use the FastAPI task catalog or `practice.py check`. Its public tests
are examples; add boundaries and record unfinished stages honestly.
Every start creates a unique folder without instructor reference code.

Do not read the following before an independent attempt:

- `templates/` contains working reference applications and public existing-behavior tests.
- `coach/starters.py` and the scenario coach modules apply one controlled defect or missing feature to
  a fresh reference copy for each task.
- `coach/contracts.py` preserves original contracts; the scenario coach modules
  supply replacement checks with HTTP behavior, side effects and boundaries.
- `catalog.py` and `scenarios/` contain learner-facing briefs, with no defective line locations.
- `legacy/` retains the original catalog and README generator for compatibility.

```sh
uv run python scripts/practice.py verify
uv run python scripts/practice.py verify --revision 1
uv run pytest
```

`verify` checks all 24 current starter/reference pairs and runs public tests on each version.
Every starter must fail a behavior assertion (an import error does not qualify),
every reference must pass, and both versions must pass their public tests. Use
`--revision 1` to check the original sequence. The platform
tests additionally verify no overwrite, no instructor leakage, no attempt
modification, traversal/symlink rejection, and failure/error distinction.

The base application scope is deliberately small: in-memory state, one server
worker, integer cents, fictitious fixtures, no persistence/authentication or
distributed concurrency. Reloading resets state. State correctness within that
scope remains part of the exercise.
