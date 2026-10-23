# Local practice system

Twenty independent tasks cover ten days. These are original fictional exercises,
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
English interview prompt, exact contract, fixture description, startup commands,
public tests and deliverables. `uv run uvicorn app.main:app --reload` runs its API
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

The public learner tests verify startup. Add regression and boundary tests before
claiming a fix. The external checks sample the published behavior; their failure
messages describe the contract without printing the hidden test source.

## Instructor and maintenance material

Do not read the following before an independent attempt:

- `templates/` contains the four working reference applications: Cedar Wallet,
  Fern Merchant Operations, Juniper Rewards and Harbor Supply.
- `coach/starters.py` applies exactly one controlled defect or missing feature to
  a fresh reference copy for each task.
- `coach/contracts.py` exercises HTTP behavior, side effects and boundaries.
- `catalog.py` contains learner-facing briefs, with no defective line locations.

```sh
uv run python scripts/practice.py verify
uv run pytest
```

`verify` checks all twenty pairs. Every starter must fail a behavior assertion
(an import error does not qualify), and every reference must pass. The platform
tests additionally verify no overwrite, no instructor leakage, no attempt
modification, traversal/symlink rejection, and failure/error distinction.

The base application scope is deliberately small: in-memory state, one server
worker, integer cents, fictitious fixtures, no persistence/authentication or
distributed concurrency. Reloading resets state. State correctness within that
scope remains part of the exercise.
