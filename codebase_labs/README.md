# Codebase Practice: Read, Test, Change

Start with [exercise 01 on CoJudge](https://cojudge.musel.dev/problems/cb-01-missing-null-zero).
Open the [course list](https://cojudge.musel.dev/?course=capital-one-codebase-practice) to continue.

This course builds technical judgment for unfamiliar Python code. You read an
existing implementation, predict its behavior, write tests, and make a small
change. You write the code and tests. AI is optional for explanations and reviews.
SQL and advanced distributed systems are not prerequisites.

The course has 16 browser exercises and eight local labs. Complete them in the
order below. Each browser exercise contains a runnable defect. Each local lab
contains a small application with several files. A lab starts from an independent
snapshot, so unfinished earlier work does not block the next task.

## The work cycle

1. Read the rule and find the entry point.
2. Follow the relevant calls, data, state, and error paths.
3. Predict one normal result and one boundary result before execution.
4. Write your test or regression case.
5. Run it before the change. Check why it passes or fails.
6. Make the assigned change yourself.
7. Run the focused checks and the full supplied suite.
8. Review the diff and compare any AI claim with your evidence.

Do one task at a time. The estimates are practice guides, not deadlines. A task
is not complete because a timer expired or a completion percentage increased.

## Ordered sequence

| Step | Exercise | Main skill |
| --- | --- | --- |
| 01 | [Browser 01: Configuration defaults](https://cojudge.musel.dev/problems/cb-01-missing-null-zero) | Trace absence, null, and zero |
| 02 | [Browser 02: Runtime validation](https://cojudge.musel.dev/problems/cb-02-typed-json-boundary) | Separate type hints from validation |
| 03 | [Browser 03: Instance state](https://cojudge.musel.dev/problems/cb-03-dataclass-list-isolation) | Find shared mutable data |
| 04 | [Browser 04: Nested copies](https://cojudge.musel.dev/problems/cb-04-nested-copy-isolation) | Track which object owns state |
| 05 | [Local lab01: Intake pipeline](briefs/lab01.md) | Navigate imports and write characterization tests |
| 06 | [Local lab02: Runtime boundary](briefs/lab02.md) | Use parametrized tests for valid and invalid inputs |
| 07 | [Browser 05: Inherited behavior](https://cojudge.musel.dev/problems/cb-05-inheritance-fee-policy) | Follow method dispatch and boundary rules |
| 08 | [Browser 06: Composed dependency](https://cojudge.musel.dev/problems/cb-06-composed-fee-protocol) | Understand a Protocol and its callers |
| 09 | [Browser 07: State transitions](https://cojudge.musel.dev/problems/cb-07-explicit-order-states) | Preserve rejected-operation behavior |
| 10 | [Browser 08: Atomic changes](https://cojudge.musel.dev/problems/cb-08-atomic-memory-batch) | Prevent partial state updates |
| 11 | [Local lab03: Queue isolation](briefs/lab03.md) | Write a regression and fix state leakage |
| 12 | [Local lab04: Fake dependency](briefs/lab04.md) | Test the caller and its exception boundary |
| 13 | [Browser 09: Request routing](https://cojudge.musel.dev/problems/cb-09-route-contract) | Trace method and path decisions |
| 14 | [Browser 10: Request validation](https://cojudge.musel.dev/problems/cb-10-body-validation) | Check a pure API boundary function |
| 15 | [Browser 11: PATCH behavior](https://cojudge.musel.dev/problems/cb-11-put-patch-fields) | Preserve field-presence semantics |
| 16 | [Browser 12: Replayed writes](https://cojudge.musel.dev/problems/cb-12-idempotency-conflicts) | Distinguish a replay from a conflict |
| 17 | [Local lab05: Validation before writes](briefs/lab05.md) | Test HTTP output, stored state, events, and IDs |
| 18 | [Local lab06: PATCH feature](briefs/lab06.md) | Add one field with compatibility tests |
| 19 | [Browser 13: Pagination order](https://cojudge.musel.dev/problems/cb-13-cursor-tie-breaks) | Test equal timestamps and cursor boundaries |
| 20 | [Browser 14: Retry policy](https://cojudge.musel.dev/problems/cb-14-retry-backoff) | Classify errors and cap delays |
| 21 | [Browser 15: Timeout budget](https://cojudge.musel.dev/problems/cb-15-shared-deadline) | Follow elapsed time across operations |
| 22 | [Browser 16: Client integration](https://cojudge.musel.dev/problems/cb-16-upstream-page-client) | Trace interacting state and failure rules |
| 23 | [Local lab07: Deterministic client tests](briefs/lab07.md) | Use a fake transport and clock without real requests |
| 24 | [Local lab08: Review an AI patch](briefs/lab08.md) | Find a regression and verify your own repair |

## Run a local lab

From this repository:

```sh
uv sync
uv run python scripts/codebase.py list
uv run python scripts/codebase.py start lab01
```

Open the printed folder. Read its README. It contains the complete rule, file map,
allowed edits, examples, hints, and commands. Each start creates a new folder.
The command does not reset an earlier attempt.

From the new attempt folder:

```sh
uv sync
uv run pytest -q tests/test_existing.py
uv run pytest -q tests/learner
```

The learner test file is empty at first. A “no tests ran” result is expected until
you write tests. Use `uv run pytest --collect-only -q tests/learner` to see which
tests pytest finds. Use `rg` to find definitions and callers. Use the traceback
to follow a failure back into application code. Inspect `pyproject.toml` to see
the Python version, dependencies, and test configuration.

After your work, run the exact check command from the attempt README. From the
repository root, its form is:

```sh
uv run python scripts/codebase.py check attempts/YOUR-ATTEMPT
```

The checker uses a temporary copy. It checks your tests against a correct
implementation and several faulty variants. Your tests must accept correct code
and detect each required defect through an assertion. Import errors and crashes
do not count as good tests. Repair and feature labs also run separate behavior
checks against your implementation.

Exit codes are **0** for sampled success, **1** for missing behavior or test
evidence, and **2** for a setup or execution error. Read the reported phase.
Preserve your tests and code in the attempt folder.

## Use AI with evidence

Use the optional prompt in each task after your own first trace. Ask for one
specific result, such as a call path with file references or a review of your
test assumptions. Keep the requested files and behavior explicit. Ask the tool
to state uncertainty. Do not ask it to implement the task or write your initial
regression test.

Check every useful claim against the code or an experiment. A plausible answer
can describe a function that does not exist, miss a side effect, or repeat a bad
assumption from the implementation. The supplied AI claims are constructed
examples. Some are correct. The task is to verify them, not reject them by default.

Before accepting a suggestion, check which requirement it serves, which callers
it can affect, which test would fail without it, and whether the diff stays in
scope. In a Git-tracked workspace, use `git diff -- path/to/file` to inspect a
change. Attempt folders are Git-ignored; use your editor's file comparison there.

## What this course covers

- Python dictionaries, type boundaries, dataclasses, ownership, and copying.
- Inheritance, composition, Protocols, callers, and state transitions.
- API routing, validation, field updates, retries, cursors, and deadlines.
- Pytest assertions, `raises`, parametrization, fixtures, and test isolation.
- Fakes, patch lookup scope, unit tests, and API integration tests.
- Regression tests, compatibility, rejected-operation state, and test limitations.
- Reading a small codebase and checking claims in AI explanations and patches.

Read the relevant official documentation when a concept is new. Pytest documents
[parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html) and
[monkeypatching](https://docs.pytest.org/en/stable/how-to/monkeypatch.html).
Python documents [mock objects](https://docs.python.org/3.12/library/unittest.mock.html).
FastAPI documents [TestClient-based tests](https://fastapi.tiangolo.com/tutorial/testing/).

The earlier [Engineering 50 course](https://cojudge.musel.dev/?course=capital-one-engineering-50)
is optional extended practice. Its SQL and distributed-system exercises are not
requirements inferred from the TDP job posting.

These are constructed exercises. They are not a confirmed Capital One interview
syllabus. Browser tasks simulate their contracts. Local API tasks use a real
framework in one process. Client tasks use fake transport and time. Finite tests
cannot prove all behavior, design quality, or readiness for an interview.

## Instructor and maintenance files

Avoid `lab*.py`, `cojudge/instructor/`, and optional solutions before an independent
attempt. These contain references and verification material. The start command
copies only the learner files and brief. To maintain the course:

```sh
uv run python scripts/codebase_course.py build
uv run python scripts/codebase_course.py verify --report /tmp/codebase-course.json
uv run python scripts/codebase.py verify --report /tmp/codebase-labs.json
uv run pytest -q
```
