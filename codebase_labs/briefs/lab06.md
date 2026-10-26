# lab06: Add a PATCH field without losing zero or null

[Back to the ordered course guide](../README.md)

**Objective:** Add one PATCH field with distinct missing, null, and zero behavior.

**Practice estimate:** 50 minutes.

Start a fresh attempt from the repository root:

```sh
uv run python scripts/codebase.py start lab06
```

Open the printed folder and follow its README. It includes the exact check command.

# Context

This constructed API has an existing ticket with an effort estimate.
The API can update its title and priority. Add support for updating
`effort_minutes` through the same PATCH route.
This is an independent snapshot. Do not copy a previous attempt into it.
The task does not add a route or change ticket creation.

## Learn first

PATCH changes selected fields. A missing key means no requested change.
JSON null becomes Python `None`. It is an explicit value.
Zero is also an explicit value. Python treats both zero and None as false
in an `if value` condition. That condition cannot express this contract.
Test key presence and value rules as separate questions.

The service reads a copy of the row. It validates changes on that copy.
The store replaces the row only after all checks pass.
This keeps a rejected request from making a partial change.
Use a route integration test to check JSON, service logic, and storage.
A fixture should create a fresh store and `TestClient(create_app(store))`.
Parameterized tests can share the operation while changing the supplied
value and the expected result. Use separate cases for missing and null.

Worked example: the stored priority is 2. PATCH `{"priority": 0}` changes
it to 0. PATCH `{}` after that keeps it at 0. The first request records
one audit event. The empty request records none.
Apply the same presence reasoning to the new field's separate rules.

## File map

- `app/__init__.py`: package marker.
- `app/main.py`: GET and PATCH routes; HTTP error mapping.
- `app/service.py`: field selection and validation before replacement.
- `app/rules.py`: existing title and priority validators.
- `app/store.py`: seeded row, copied reads, and update audit events.
- `tests/test_existing.py`: existing API behavior.
- `tests/learner/test_task.py`: your empty test file.

## Read and trace

Run `rg -n 'patch_ticket|replace|effort_minutes' app`.
Trace a title update from the route to the store.
Locate the difference between the local row copy and the stored row.
Identify why the current service rejects the new field.

## Assignment and allowed edits

Write the first failing test yourself under `tests/learner/`.
Add the field in `app/service.py`. Only those paths are editable.
Keep title, priority, empty PATCH, unknown-field, and missing-ticket behavior.
Keep validation before the single write. Do not change public tests.
Do not add a schema library, endpoint, database, or automatic conversion.

## Exact accepted and rejected behavior

The fresh row is `{"id": 1, "title": "Printer", "priority": 2,
"effort_minutes": 30}`. The initial audit list is empty.
GET `/tickets/1` returns that current row with 200.
PATCH `/tickets/{id}` accepts a JSON object with title, priority, and/or
effort_minutes. Every successful PATCH returns the full row with 200.

- Missing `effort_minutes`: preserve the stored value, including None or 0.
- Explicit null: store None to clear the estimate.
- An exact integer from 0 through 240: store that integer.
- Reject booleans, floats, strings, lists, objects, negative integers, and
  integers above 240. Return 422 with `{"detail": "invalid effort_minutes"}`.
- Missing title or priority: preserve its stored value.
- Title: a string with 1 to 80 characters after stripping; store it stripped.
- Priority: an exact integer from 0 through 3. Null and booleans are invalid.

Existing error messages are `invalid title`, `invalid priority`, and
`unknown field`. All use status 422 and a `detail` key.
Error order is missing ticket, unknown key, title, priority, effort.
An unknown ticket returns 404 with `{"detail": "ticket not found"}`,
even if its body has invalid field values.
Reject the whole update if any field fails. Preserve the row and audit.
Every accepted nonempty object records one `("updated", id)` event,
even if it repeats stored values. An empty object records no event.
Non-object JSON bodies use FastAPI validation. Its detailed error shape
is outside this assignment.

## Examples

Starting from effort 30, `{}` keeps 30 with no audit event.
`{"effort_minutes": null}` clears it. A later title-only update keeps None.
`{"effort_minutes": 0}` stores 0. It does not keep the previous estimate.
`{"title": "Cable", "effort_minutes": 241}` rejects both changes.
`{"title": " Cable ", "priority": 0, "effort_minutes": 12}` updates all
three fields and creates one event.

## Boundary checklist

- Positive effort: detect the starter's unsupported-field behavior.
- Null over an existing 30: detect ignored clear requests.
- Zero over an existing 30: detect truthiness-based fallback.
- True and false: detect Python boolean acceptance as integers.
- Limits 0 and 240; rejected -1 and 241: check the inclusive range.
- Missing after clearing or setting zero: preserve existing values.
- Valid title plus invalid effort: detect partial mutation.
- Existing null rejections, empty body, unknown key, and unknown ID:
  protect compatibility.

## Focused commands and pytest techniques

Run from the attempt directory. No server is required.
Run `uv run pytest --collect-only -q tests/learner`.
Run `uv run pytest -q tests/learner`.
Run `uv run pytest -q` after the change.
Use `@pytest.mark.parametrize` for input classes, not only positive values.
Use direct expected dictionaries. Do not call the validator to calculate
the expected answer. Check the response and a later GET separately.
Use `git diff -- app/service.py tests/learner` when files are tracked.
Otherwise compare a saved file with `git diff --no-index OLD NEW`.

## Optional AI review prompt

"Review my PATCH tests and diff. Cite the file and branch for missing,
null, zero, and boolean input. Check old title and priority behavior.
Ask about one unsupported assumption. Do not write code or tests."

Constructed AI claim to check: "Using the submitted estimate or the
stored estimate handles both missing fields and zero safely."

## Hints

1. `body.get` without a sentinel combines missing and explicit None.
2. Existing field branches show how field presence differs from validity.
3. Validation belongs before `store.replace`.

## Technical done checks

Your new-field regression failed on the starter.
Your tests cover missing, null, zero, limits, and atomic rejection.
Your implementation passes your tests and the public suite.
Review the diff. Run the guide's local checker against this attempt.
This model excludes concurrent updates, persistence, and version conflicts.
Official references: [FastAPI partial updates](https://fastapi.tiangolo.com/tutorial/body-updates/)
and [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/).

## Check the AI claim

This is a constructed example. Assess it with code and tests.

> body.get('effort_minutes') or row['effort_minutes'] preserves missing fields and handles zero.

## Official references

- [Documentation 1](https://fastapi.tiangolo.com/tutorial/body-updates/)
- [Documentation 2](https://fastapi.tiangolo.com/tutorial/testing/)
