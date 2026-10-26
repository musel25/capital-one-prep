# lab05: Validate a ticket before the first write

[Back to the ordered course guide](../README.md)

**Objective:** Trace an HTTP request and prevent state changes when validation fails.

**Practice estimate:** 45 minutes.

Start a fresh attempt from the repository root:

```sh
uv run python scripts/codebase.py start lab05
```

Open the printed folder and follow its README. It includes the exact check command.

# Context

This is a constructed ticket API. It is not an employer question.
A rejected create request must leave all stored state unchanged.
The starter returns an error for an invalid priority, but it writes first.
Your task is one repair: make validation finish before any write.
You will write the regression tests and the repair yourself.

## Learn first

A route maps an HTTP method and path to a function.
`POST /tickets` receives a JSON object. It calls validation helpers.
The store assigns an ID, stores a row, and records an audit event.
An audit event is a record that an operation occurred.
Those three changes are side effects. An HTTP error does not undo them.

`TestClient` calls the app in the test process. It needs no running server.
Create a fresh `TicketStore` for each test. Pass it to `create_app(store)`.
A pytest fixture can build this pair and yield it to each test.
A unit test checks one helper. An integration test follows the route into
the store. Use integration tests for this task.
Check the response with `response.status_code` and `response.json()`.
Check state through `GET /tickets`, `store.audit`, and the next accepted ID.

Worked trace: `{"title": "  Cable  ", "priority": 0}` becomes
`{"id": 1, "title": "Cable", "priority": 0}` in a fresh store.
The response status is 201. The audit list becomes `[("created", 1)]`.
Priority 0 is a valid value. It is not a request for the default.

## File map

- `app/__init__.py`: package marker.
- `app/main.py`: app factory and HTTP routes.
- `app/rules.py`: title and priority validation.
- `app/store.py`: rows, ID allocation, and audit events.
- `tests/test_existing.py`: supported behavior and assert syntax.
- `tests/learner/test_task.py`: your empty test file.

## Read and trace

Run `rg -n 'create_ticket|insert|priority_value' app`.
Follow one accepted request and one rejected request.
Locate the first state change. List each state value that it changes.
Read the helper before changing its caller.

## Assignment and allowed edits

Write your own failing regression in `tests/learner/test_task.py` first.
Predict the row list, audit list, and next accepted ID before running it.
Repair `app/main.py`. You may add test files under `tests/learner/`.
Do not change the store, validation helpers, or public tests.
Preserve the existing routes, status codes, and response shape.
Do not add rollback logic, a database, authentication, or a new endpoint.

## Exact accepted and rejected behavior

The body is a JSON object. Only `title` and `priority` are allowed.
Title is required. It must be a string with 1 to 80 characters after
`.strip()`. Store the stripped title.
Priority defaults to 1 only when its key is absent.
Priority must be an integer from 0 through 3. Reject booleans, floats,
strings, null, lists, objects, and integers outside that range.
Check unknown fields first, then title, then priority.
Invalid objects return 422 and `{"detail": MESSAGE}`. Messages are:

- Unknown key: `unknown field`.
- Invalid title: `title must be 1 to 80 nonblank characters`.
- Invalid priority: `priority must be an integer from 0 to 3`.

A rejection changes no rows, audit events, or next ID.
An acceptance returns 201 and the stored row. It allocates exactly one ID
and appends exactly one `("created", id)` event. IDs start at 1.
`GET /tickets` returns rows in ID order. Each app factory call has fresh
state unless you pass a store. Non-object bodies use FastAPI validation;
its detailed error payload is outside this assignment.

## Examples

In a fresh store, accept `{"title": "Router"}` as ID 1, priority 1.
Then reject `{"title": "Switch", "priority": -1}` with 422.
`GET /tickets` must still contain only Router.
The next accepted ticket must have ID 2.
`{"title": "Switch", "priority": null}` is rejected, not defaulted.

## Boundary checklist

- Late invalid priority after a valid title: detect writes before validation.
- Invalid request after an existing row: detect damage to stored state.
- `true`, `false`, null, float, and string: detect permissive numeric checks.
- Priorities 0 and 3: preserve accepted limits.
- Padded title: detect loss of normalization.
- Unknown key and blank title: preserve earlier rejections.
- Rejection followed by acceptance: detect consumed IDs and audit events.

## Focused commands and pytest techniques

Run all commands from this attempt directory. No server is required.
Run `uv run pytest --collect-only -q tests/learner` to check collection.
Run `uv run pytest -q tests/learner` to run your tests.
Run `uv run pytest -q` to include the public tests.
Use `@pytest.mark.parametrize` for several invalid priority classes.
Read the final assert in a traceback before changing code.
Check the expected value against the product rule.
Use `git diff -- app tests/learner` if this directory is tracked by Git.
Use `git diff --no-index OLD NEW` to compare saved files otherwise.

## Optional AI review prompt

"Review my test and diff. Trace the POST route to every state change.
Cite file names and functions. Identify one missing rejection check.
Do not write tests, replacement code, or the repair. Limit the review to
validation order and preserved behavior."

Constructed AI claim to check: "A FastAPI HTTPException rolls back writes
made earlier in the route, so a 422 assertion proves that state is safe."

## Hints

1. A failure response proves only the response behavior.
2. A copy of a returned row does not reverse changes to the store.
3. Compare the last validation call with the first mutation call.

## Technical done checks

Your regression fails on the starter through a normal assertion.
Your tests pass after your repair. The public tests still pass.
Your tests check response data and state. You reviewed the small diff.
Run the guide's local checker against this attempt.
Passing sampled checks does not prove all behavior or interview readiness.
This model has no concurrency, persistence, or real network.
Official references: [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
and [pytest parameters](https://docs.pytest.org/en/stable/how-to/parametrize.html).

## Check the AI claim

This is a constructed example. Assess it with code and tests.

> An HTTPException rolls back earlier writes, so checking 422 proves the store is unchanged.

## Official references

- [Documentation 1](https://fastapi.tiangolo.com/tutorial/testing/)
- [Documentation 2](https://docs.pytest.org/en/stable/how-to/parametrize.html)
