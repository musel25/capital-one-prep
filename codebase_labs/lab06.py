"""Instructor data for PATCH field-presence practice."""

from textwrap import dedent


STORE = dedent('''\
class TicketStore:
    def __init__(self):
        self.rows = {1: {"id": 1, "title": "Printer", "priority": 2, "effort_minutes": 30}}
        self.audit = []

    def get(self, ticket_id):
        row = self.rows.get(ticket_id)
        return None if row is None else row.copy()

    def replace(self, ticket_id, row):
        self.rows[ticket_id] = row.copy()
        self.audit.append(("updated", ticket_id))
        return row.copy()
''')

RULES = dedent('''\
def title_value(value):
    if not isinstance(value, str) or not 1 <= len(value.strip()) <= 80:
        raise ValueError("invalid title")
    return value.strip()


def priority_value(value):
    if type(value) is not int or not 0 <= value <= 3:
        raise ValueError("invalid priority")
    return value
''')

MAIN = dedent('''\
from fastapi import Body, FastAPI, HTTPException

from app.service import patch_ticket
from app.store import TicketStore


def create_app(store=None):
    store = TicketStore() if store is None else store
    app = FastAPI()

    @app.get("/tickets/{ticket_id}")
    def get_ticket(ticket_id: int):
        row = store.get(ticket_id)
        if row is None:
            raise HTTPException(status_code=404, detail="ticket not found")
        return row

    @app.patch("/tickets/{ticket_id}")
    def update_ticket(ticket_id: int, body: dict = Body(...)):
        try:
            return patch_ticket(store, ticket_id, body)
        except KeyError as error:
            raise HTTPException(status_code=404, detail="ticket not found") from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    return app
''')

STARTER = dedent('''\
from app.rules import priority_value, title_value


def patch_ticket(store, ticket_id, body):
    row = store.get(ticket_id)
    if row is None:
        raise KeyError(ticket_id)
    if set(body) - {"title", "priority"}:
        raise ValueError("unknown field")
    if "title" in body:
        row["title"] = title_value(body["title"])
    if "priority" in body:
        row["priority"] = priority_value(body["priority"])
    if not body:
        return row
    return store.replace(ticket_id, row)
''')

FIELD_UPDATE = dedent('''\
    if "effort_minutes" in body:
        value = body["effort_minutes"]
        if value is not None and (type(value) is not int or not 0 <= value <= 240):
            raise ValueError("invalid effort_minutes")
        row["effort_minutes"] = value
''')
# Keep the injected block at function indentation.
FIELD_UPDATE = "".join("    " + line if line.strip() else line for line in FIELD_UPDATE.splitlines(keepends=True))
CORRECT = STARTER.replace('{"title", "priority"}', '{"title", "priority", "effort_minutes"}').replace(
    "    if not body:\n", FIELD_UPDATE + "    if not body:\n"
)

PUBLIC = dedent('''\
from fastapi.testclient import TestClient

from app.main import create_app
from app.store import TicketStore


def test_existing_fields_can_change_together():
    store = TicketStore()
    with TestClient(create_app(store)) as client:
        response = client.patch("/tickets/1", json={"title": "  Scanner  ", "priority": 0})
        assert response.status_code == 200
        assert response.json() == {"id": 1, "title": "Scanner", "priority": 0, "effort_minutes": 30}
    assert store.audit == [("updated", 1)]


def test_unknown_ticket_uses_404():
    with TestClient(create_app()) as client:
        response = client.patch("/tickets/99", json={"title": "New"})
        assert response.status_code == 404
        assert response.json() == {"detail": "ticket not found"}
''')

CONTRACT_TESTS = dedent('''\
import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.store import TicketStore


@pytest.mark.parametrize("body,effort,title,priority,events", [
    ({}, 30, "Printer", 2, []),
    ({"title": " New "}, 30, "New", 2, [("updated", 1)]),
    ({"priority": 0}, 30, "Printer", 0, [("updated", 1)]),
    ({"effort_minutes": None}, None, "Printer", 2, [("updated", 1)]),
    ({"effort_minutes": 0}, 0, "Printer", 2, [("updated", 1)]),
    ({"effort_minutes": 240}, 240, "Printer", 2, [("updated", 1)]),
    ({"effort_minutes": 12, "priority": 3, "title": " Cable "}, 12, "Cable", 3, [("updated", 1)]),
])
def test_patch_contract(body, effort, title, priority, events):
    store = TicketStore()
    expected = {"id": 1, "title": title, "priority": priority, "effort_minutes": effort}
    with TestClient(create_app(store)) as api:
        response = api.patch("/tickets/1", json=body)
        assert (response.status_code, response.json()) == (200, expected)
        assert api.get("/tickets/1").json() == expected
        assert store.audit == events


@pytest.mark.parametrize("value", [True, False, -1, 241, 1.0, "2", [], {}])
def test_invalid_effort_rejects_all_field_changes(value):
    store = TicketStore()
    with TestClient(create_app(store)) as api:
        before = api.get("/tickets/1").json()
        response = api.patch("/tickets/1", json={"title": "Changed", "priority": 0, "effort_minutes": value})
        assert (response.status_code, response.json()) == (422, {"detail": "invalid effort_minutes"})
        assert api.get("/tickets/1").json() == before
        assert store.audit == []


@pytest.mark.parametrize("body,message", [
    ({"title": None, "effort_minutes": 0}, "invalid title"),
    ({"title": " ", "effort_minutes": 0}, "invalid title"),
    ({"priority": None, "effort_minutes": 0}, "invalid priority"),
    ({"priority": True, "effort_minutes": 0}, "invalid priority"),
    ({"priority": 4, "effort_minutes": 0}, "invalid priority"),
    ({"other": 4, "effort_minutes": 0}, "unknown field"),
])
def test_existing_rejections_remain_atomic(body, message):
    store = TicketStore()
    with TestClient(create_app(store)) as api:
        response = api.patch("/tickets/1", json=body)
        assert (response.status_code, response.json()) == (422, {"detail": message})
        assert store.get(1) == {"id": 1, "title": "Printer", "priority": 2, "effort_minutes": 30}
        assert store.audit == []


def test_missing_after_clear_preserves_none_and_missing_ticket_wins():
    store = TicketStore()
    with TestClient(create_app(store)) as api:
        api.patch("/tickets/1", json={"effort_minutes": None})
        response = api.patch("/tickets/1", json={"title": "Kept"})
        assert response.json()["effort_minutes"] is None
        assert store.audit == [("updated", 1), ("updated", 1)]
        response = api.patch("/tickets/2", json={"effort_minutes": True})
        assert (response.status_code, response.json()) == (404, {"detail": "ticket not found"})
        assert len(store.audit) == 2
''')

REFERENCE_TESTS = dedent('''\
import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.store import TicketStore


@pytest.fixture
def api_and_store():
    store = TicketStore()
    with TestClient(create_app(store)) as api:
        yield api, store


@pytest.mark.parametrize("new_value", [None, 0, 1, 240])
def test_effort_presence_has_exact_meaning(api_and_store, new_value):
    api, store = api_and_store
    result = api.patch("/tickets/1", json={"effort_minutes": new_value})
    expected = {"id": 1, "title": "Printer", "priority": 2, "effort_minutes": new_value}
    assert result.status_code == 200
    assert result.json() == expected
    assert api.get("/tickets/1").json() == expected
    assert store.audit == [("updated", 1)]
    unchanged = api.patch("/tickets/1", json={"priority": 0})
    assert unchanged.json()["effort_minutes"] == new_value


@pytest.mark.parametrize("bad", [True, False, -5, 241, 0.0, "0", [], {}])
def test_bad_effort_prevents_partial_write(api_and_store, bad):
    api, store = api_and_store
    response = api.patch("/tickets/1", json={"title": "Other", "effort_minutes": bad})
    assert response.status_code == 422
    assert response.json() == {"detail": "invalid effort_minutes"}
    assert store.get(1) == {"id": 1, "title": "Printer", "priority": 2, "effort_minutes": 30}
    assert store.audit == []


def test_existing_fields_and_empty_patch(api_and_store):
    api, store = api_and_store
    empty = api.patch("/tickets/1", json={})
    assert empty.status_code == 200
    assert empty.json()["effort_minutes"] == 30
    assert store.audit == []
    mixed = api.patch("/tickets/1", json={"title": "  Cable  ", "priority": 3, "effort_minutes": 22})
    assert mixed.json() == {"id": 1, "title": "Cable", "priority": 3, "effort_minutes": 22}
    assert store.audit == [("updated", 1)]
    for body in ({"title": None}, {"priority": None}, {"wrong": 1}):
        assert api.patch("/tickets/1", json=body).status_code == 422
    assert store.get(1) == mixed.json()
    assert store.audit == [("updated", 1)]
''')

LAB = {
    "id": "lab06",
    "title": "Add a PATCH field without losing zero or null",
    "kind": "feature",
    "after": 12,
    "minutes": 50,
    "objective": "Add one PATCH field with distinct missing, null, and zero behavior.",
    "brief": dedent('''\
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
        '''),
    "editable": ["app/service.py", "tests/learner/"],
    "files": {
        "app/__init__.py": "",
        "app/main.py": MAIN,
        "app/service.py": STARTER,
        "app/rules.py": RULES,
        "app/store.py": STORE,
        "tests/test_existing.py": PUBLIC,
        "tests/learner/test_task.py": '"""Write your own tests here."""\n',
    },
    "reference": {"app/service.py": CORRECT},
    "contract_tests": CONTRACT_TESTS,
    "reference_tests": REFERENCE_TESTS,
    "variants": [
        {"name": "rejects the new field", "files": {"app/service.py": STARTER}},
        {"name": "ignores explicit null", "files": {"app/service.py": CORRECT.replace(
            'if "effort_minutes" in body:', 'if "effort_minutes" in body and body["effort_minutes"] is not None:'
        )}},
        {"name": "falls back when effort is zero", "files": {"app/service.py": CORRECT.replace(
            'row["effort_minutes"] = value', 'row["effort_minutes"] = (value or row["effort_minutes"]) if value is not None else None'
        )}},
        {"name": "accepts boolean effort", "files": {"app/service.py": CORRECT.replace(
            'type(value) is not int', 'not isinstance(value, int)'
        )}},
    ],
    "ai_claim": "body.get('effort_minutes') or row['effort_minutes'] preserves missing fields and handles zero.",
    "ai_answer": "False. With stored effort 30 and a submitted effort of 0, that expression returns 30. It also returns 30 for explicit null, which must clear the value. Missing, null, and zero need distinct contract checks.",
    "sources": [
        "https://fastapi.tiangolo.com/tutorial/body-updates/",
        "https://fastapi.tiangolo.com/tutorial/testing/",
    ],
}
