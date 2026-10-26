"""Instructor data for the validation-before-write ticket lab."""

from textwrap import dedent


STORE = dedent('''\
class TicketStore:
    def __init__(self):
        self.rows = {}
        self.next_id = 1
        self.audit = []

    def insert(self, title, priority):
        ticket_id = self.next_id
        self.next_id += 1
        row = {"id": ticket_id, "title": title, "priority": priority}
        self.rows[ticket_id] = row.copy()
        self.audit.append(("created", ticket_id))
        return row.copy()

    def all(self):
        return [self.rows[key].copy() for key in sorted(self.rows)]
''')

RULES = dedent('''\
def title_value(value):
    if not isinstance(value, str) or not 1 <= len(value.strip()) <= 80:
        raise ValueError("title must be 1 to 80 nonblank characters")
    return value.strip()


def priority_value(value):
    if type(value) is not int or not 0 <= value <= 3:
        raise ValueError("priority must be an integer from 0 to 3")
    return value
''')

CORRECT = dedent('''\
from fastapi import Body, FastAPI, HTTPException

from app.rules import priority_value, title_value
from app.store import TicketStore


def create_app(store=None):
    store = TicketStore() if store is None else store
    app = FastAPI()

    @app.get("/tickets")
    def list_tickets():
        return store.all()

    @app.post("/tickets", status_code=201)
    def create_ticket(body: dict = Body(...)):
        try:
            if set(body) - {"title", "priority"}:
                raise ValueError("unknown field")
            title = title_value(body.get("title"))
            priority = priority_value(body.get("priority", 1))
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        return store.insert(title, priority)

    return app
''')

STARTER = CORRECT.replace(
    '            priority = priority_value(body.get("priority", 1))',
    '            row = store.insert(title, body.get("priority", 1))\n'
    '            priority_value(row["priority"])',
).replace('        return store.insert(title, priority)', '        return row')

PUBLIC = dedent('''\
from fastapi.testclient import TestClient

from app.main import create_app
from app.store import TicketStore


def test_create_and_list_supported_ticket():
    store = TicketStore()
    with TestClient(create_app(store)) as client:
        response = client.post("/tickets", json={"title": "  Replace cable  "})
        assert response.status_code == 201
        assert response.json() == {"id": 1, "title": "Replace cable", "priority": 1}
        assert client.get("/tickets").json() == [response.json()]
    assert store.audit == [("created", 1)]


def test_blank_title_is_rejected():
    with TestClient(create_app()) as client:
        response = client.post("/tickets", json={"title": "   "})
        assert response.status_code == 422
''')

CONTRACT_TESTS = dedent('''\
import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.store import TicketStore


@pytest.mark.parametrize("value", [None, True, False, -1, 4, 1.0, "1", [], {}])
def test_rejected_priority_has_no_side_effect(value):
    store = TicketStore()
    with TestClient(create_app(store)) as api:
        api.post("/tickets", json={"title": "First", "priority": 2})
        rejected = api.post("/tickets", json={"title": "Bad", "priority": value})
        assert rejected.status_code == 422
        assert rejected.json() == {"detail": "priority must be an integer from 0 to 3"}
        assert api.get("/tickets").json() == [{"id": 1, "title": "First", "priority": 2}]
        assert store.audit == [("created", 1)]
        assert store.next_id == 2
        assert api.post("/tickets", json={"title": "Next"}).json()["id"] == 2


@pytest.mark.parametrize("value", [0, 1, 2, 3])
def test_valid_priority_and_normalized_title(value):
    store = TicketStore()
    with TestClient(create_app(store)) as api:
        result = api.post("/tickets", json={"title": "  Check port  ", "priority": value})
        assert result.status_code == 201
        assert result.json() == {"id": 1, "title": "Check port", "priority": value}
        assert store.all() == [result.json()]
        assert store.audit == [("created", 1)]


@pytest.mark.parametrize("body,detail", [
    ({}, "title must be 1 to 80 nonblank characters"),
    ({"title": None}, "title must be 1 to 80 nonblank characters"),
    ({"title": 4}, "title must be 1 to 80 nonblank characters"),
    ({"title": "  "}, "title must be 1 to 80 nonblank characters"),
    ({"title": "x" * 81}, "title must be 1 to 80 nonblank characters"),
    ({"title": "Fine", "extra": 3}, "unknown field"),
])
def test_other_rejections_are_atomic(body, detail):
    store = TicketStore()
    with TestClient(create_app(store)) as api:
        result = api.post("/tickets", json=body)
        assert (result.status_code, result.json()) == (422, {"detail": detail})
        assert api.get("/tickets").json() == []
        assert (store.next_id, store.audit) == (1, [])


def test_maximum_title_and_fresh_app_state():
    with TestClient(create_app()) as first, TestClient(create_app()) as second:
        accepted = first.post("/tickets", json={"title": " " + "x" * 80 + " "})
        assert accepted.status_code == 201
        assert accepted.json()["title"] == "x" * 80
        assert second.get("/tickets").json() == []
''')

REFERENCE_TESTS = dedent('''\
import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.store import TicketStore


@pytest.fixture
def ticket_api():
    store = TicketStore()
    with TestClient(create_app(store)) as client:
        yield client, store


@pytest.mark.parametrize("bad_priority", [-2, 9, True, False, None, "0", 2.5])
def test_invalid_request_preserves_rows_audit_and_identity(ticket_api, bad_priority):
    client, store = ticket_api
    saved = client.post("/tickets", json={"title": "Saved"}).json()
    response = client.post("/tickets", json={"title": "Rejected", "priority": bad_priority})
    assert response.status_code == 422
    assert response.json() == {"detail": "priority must be an integer from 0 to 3"}
    assert client.get("/tickets").json() == [saved]
    assert store.audit == [("created", 1)]
    followup = client.post("/tickets", json={"title": "Followup", "priority": 0})
    assert followup.json()["id"] == 2


@pytest.mark.parametrize("priority", [0, 3])
def test_valid_boundary_values_are_stored_exactly(ticket_api, priority):
    client, store = ticket_api
    response = client.post("/tickets", json={"title": "  Restart modem  ", "priority": priority})
    expected = {"id": 1, "title": "Restart modem", "priority": priority}
    assert response.status_code == 201
    assert response.json() == expected
    assert store.all() == [expected]
    assert store.audit == [("created", 1)]


def test_other_invalid_fields_do_not_write(ticket_api):
    client, store = ticket_api
    for body in ({"title": None}, {"title": ""}, {"title": "ok", "other": 0}):
        assert client.post("/tickets", json=body).status_code == 422
    assert client.get("/tickets").json() == []
    assert store.audit == []
''')

LAB = {
    "id": "lab05",
    "title": "Validate a ticket before the first write",
    "kind": "repair",
    "after": 12,
    "minutes": 45,
    "objective": "Trace an HTTP request and prevent state changes when validation fails.",
    "brief": dedent('''\
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
        '''),
    "editable": ["app/main.py", "tests/learner/"],
    "files": {
        "app/__init__.py": "",
        "app/main.py": STARTER,
        "app/rules.py": RULES,
        "app/store.py": STORE,
        "tests/test_existing.py": PUBLIC,
        "tests/learner/test_task.py": '"""Write your own tests here."""\n',
    },
    "reference": {"app/main.py": CORRECT},
    "contract_tests": CONTRACT_TESTS,
    "reference_tests": REFERENCE_TESTS,
    "variants": [
        {"name": "writes before priority validation", "files": {"app/main.py": STARTER}},
        {"name": "accepts boolean priorities", "files": {"app/rules.py": RULES.replace(
            "type(value) is not int", "not isinstance(value, int)"
        )}},
        {"name": "stores padded titles", "files": {"app/rules.py": RULES.replace(
            "return value.strip()", "return value"
        )}},
    ],
    "ai_claim": "An HTTPException rolls back earlier writes, so checking 422 proves the store is unchanged.",
    "ai_answer": "False. POST {title: 'Bad', priority: -1} returns 422 in the starter, but inserts ID 1, advances next_id to 2, and appends ('created', 1). HTTPException constructs an error response. It does not reverse Python object mutations.",
    "sources": [
        "https://fastapi.tiangolo.com/tutorial/testing/",
        "https://docs.pytest.org/en/stable/how-to/parametrize.html",
    ],
}
