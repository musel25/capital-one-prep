"""Instructor data for fake dependencies and a narrow exception boundary."""

from textwrap import dedent


CONTRACT_TESTS = dedent('''\
    import pytest
    from app.errors import GatewayUnavailable
    from app.service import IntakeService


    class ContractGateway:
        def __init__(self, outcome):
            self.outcome = outcome
            self.calls = []

        def send(self, record):
            self.calls.append(dict(record))
            if isinstance(self.outcome, Exception):
                raise self.outcome
            return self.outcome


    @pytest.mark.parametrize("options, retry_count", [({}, 2), ({"retries": None}, 2), ({"retries": 0}, 0), ({"retries": 5}, 5)])
    def test_normalized_payload_and_exactly_one_dependency_call(options, retry_count):
        gateway = ContractGateway("proof-7")
        payload = {"owner": "  NORA ", **options, "extra": "ignore"}
        before = dict(payload)
        response = IntakeService(gateway).submit(payload)
        assert response == {"status": "accepted", "owner": "nora", "receipt": "proof-7"}
        assert gateway.calls == [{"owner": "nora", "retries": retry_count}]
        assert payload == before


    def test_known_dependency_failure_becomes_retry_without_another_call():
        gateway = ContractGateway(GatewayUnavailable("offline"))
        assert IntakeService(gateway).submit({"owner": " NoRA "}) == {
            "status": "retry", "owner": "nora"
        }
        assert gateway.calls == [{"owner": "nora", "retries": 2}]


    @pytest.mark.parametrize("error", [ValueError("bad adapter"), RuntimeError("broken"), TypeError("bad call")])
    def test_unexpected_dependency_failure_propagates(error):
        gateway = ContractGateway(error)
        with pytest.raises(type(error)) as caught:
            IntakeService(gateway).submit({"owner": "nora"})
        assert caught.value is error
        assert gateway.calls == [{"owner": "nora", "retries": 2}]


    @pytest.mark.parametrize("payload", [
        {}, {"owner": " "}, {"owner": None}, {"owner": 8},
        {"owner": "nora", "retries": True},
        {"owner": "nora", "retries": -1},
        {"owner": "nora", "retries": 6},
        {"owner": "nora", "retries": "2"},
    ])
    def test_validation_rejects_before_dependency_side_effects(payload):
        gateway = ContractGateway("unused")
        before = dict(payload)
        with pytest.raises(ValueError):
            IntakeService(gateway).submit(payload)
        assert gateway.calls == []
        assert payload == before
''')

REFERENCE_TESTS = dedent('''\
    import pytest
    from app.errors import GatewayUnavailable
    from app.service import IntakeService


    class RecordingGateway:
        def __init__(self, *, receipt="receipt-fake", error=None):
            self.receipt = receipt
            self.error = error
            self.calls = []

        def send(self, record):
            self.calls.append(dict(record))
            if self.error is not None:
                raise self.error
            return self.receipt


    def test_caller_sends_one_normalized_record_and_preserves_input():
        gateway = RecordingGateway(receipt="chosen-9")
        payload = {"owner": "  ALEX ", "retries": 0, "note": "local"}
        assert IntakeService(gateway).submit(payload) == {
            "status": "accepted", "owner": "alex", "receipt": "chosen-9"
        }
        assert gateway.calls == [{"owner": "alex", "retries": 0}]
        assert payload == {"owner": "  ALEX ", "retries": 0, "note": "local"}


    def test_known_failure_has_no_receipt_and_no_retry_call():
        gateway = RecordingGateway(error=GatewayUnavailable("offline"))
        assert IntakeService(gateway).submit({"owner": "alex"}) == {
            "status": "retry", "owner": "alex"
        }
        assert gateway.calls == [{"owner": "alex", "retries": 2}]


    @pytest.mark.parametrize("error", [ValueError("adapter bug"), TypeError("bad result")])
    def test_unexpected_exception_is_not_hidden(error):
        gateway = RecordingGateway(error=error)
        with pytest.raises(type(error)) as caught:
            IntakeService(gateway).submit({"owner": "alex"})
        assert caught.value is error
        assert len(gateway.calls) == 1


    def test_invalid_input_never_calls_gateway():
        gateway = RecordingGateway()
        with pytest.raises(ValueError):
            IntakeService(gateway).submit({"owner": " \t ", "retries": 1})
        assert gateway.calls == []
''')

VALIDATION = dedent('''\
    """Validate before a dependency can cause a side effect."""


    def prepare_payload(payload: dict) -> dict:
        owner = payload.get("owner")
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("owner must be a nonblank string")
        retries = payload.get("retries")
        if retries is None:
            retries = 2
        if type(retries) is not int or not 0 <= retries <= 5:
            raise ValueError("retries must be an integer from 0 through 5")
        return {"owner": owner.strip().lower(), "retries": retries}
''')

SERVICE = dedent('''\
    """Coordinate validation and one gateway call."""
    from app.errors import GatewayUnavailable
    from app.gateway import Gateway
    from app.validation import prepare_payload


    class IntakeService:
        def __init__(self, gateway: Gateway):
            self.gateway = gateway

        def submit(self, payload: dict) -> dict:
            record = prepare_payload(payload)
            try:
                receipt = self.gateway.send(record)
            except GatewayUnavailable:
                return {"status": "retry", "owner": record["owner"]}
            return {
                "status": "accepted",
                "owner": record["owner"],
                "receipt": receipt,
            }
''')

LAB = {
    "id": "lab04",
    "title": "Test a caller with a fake dependency",
    "kind": "tests",
    "after": 8,
    "minutes": 40,
    "objective": "Test real caller behavior with an injected fake and a narrow exception boundary.",
    "brief": dedent('''\
        ## Context

        This is a constructed exercise. It is not a Capital One question.
        The intake service validates a request and sends a record through a gateway.
        This independent snapshot is correct. Your task is to test the caller.
        A gateway is the boundary through which the service sends data.
        This lab has no real network, timer, persistence, or automatic retry loop.

        ## Learn first

        A dependency is an object that another object calls to do part of its work.
        Dependency injection means passing that object into the caller.
        `IntakeService(gateway)` makes this boundary explicit.
        A fake is a small test implementation of that boundary.
        It can record calls, return a chosen receipt, or raise a chosen exception.
        Keep `IntakeService.submit` and real validation in the test path.

        Work through a success example.
        The input owner `"  REI "` becomes `"rei"`.
        With no retries key, the gateway receives `{"owner": "rei", "retries": 2}`.
        If the gateway returns `"r-12"`, the service returns
        `{"status": "accepted", "owner": "rei", "receipt": "r-12"}`.
        One recorded call proves that this real caller sent one record.
        Calling the fake directly would only test the fake.

        An exception boundary determines which failures a caller handles.
        Here, only `GatewayUnavailable` becomes a retry result.
        Other exceptions must stay visible to the calling code.
        A result named `"retry"` does not mean that the service makes another call.

        ## File map

        - `app/__init__.py`: package marker.
        - `app/service.py`: `IntakeService`, the real caller under test.
        - `app/validation.py`: `prepare_payload`, validation and normalization.
        - `app/gateway.py`: `Gateway` protocol and a local `MemoryGateway`.
        - `app/errors.py`: `GatewayUnavailable`, the one handled exception class.
        - `tests/test_existing.py`: a supported path with the local gateway.
        - `tests/learner/test_task.py`: your fake and your tests.

        ## Read and trace

        Run `rg -n "def |send|except|prepare_payload" app`.
        Trace validation, the dependency call, and both return paths.
        Inspect which code is inside the `try` block.
        Predict what happens when the gateway raises `ValueError`.
        Compare that with invalid input that raises before a gateway call.

        ## Assignment and allowed edits

        Write a small fake and your own tests in `tests/learner/`.
        Pass the fake to the real `IntakeService` constructor.
        Test success, the handled exception, an unexpected exception, and invalid input.
        Assert exact calls and arguments where the contract requires them.
        Do not replace the service, its `submit` method, or the validator with a fake.
        Only `tests/learner/` is editable.

        ## Exact behavior

        Input is a built-in dictionary. Other container types are outside scope.
        Owner is required and must be a string with text after `strip()`.
        Normalize it with `strip().lower()`.
        A missing owner, non-string owner, or blank owner raises `ValueError`.
        Missing or `None` retries means `2`.
        Other retry values must be built-in integers from `0` through `5`.
        Booleans, strings, floats, and out-of-range integers raise `ValueError`.
        Error-message text is not part of the contract.
        Ignore unknown keys. Keep the caller's dictionary unchanged on all paths.

        Invalid input must produce zero gateway calls.
        Valid input must produce exactly one `gateway.send(record)` call.
        Its argument must contain exactly the normalized `owner` and `retries`.
        The gateway returns a receipt string or raises an exception.
        A receipt produces exactly `status`, `owner`, and `receipt` in the response.
        Use status `"accepted"` and preserve the exact receipt string.
        `GatewayUnavailable`, including its subclasses, produces exactly
        `{"status": "retry", "owner": <normalized owner>}`.
        Do not include a receipt on that path. Do not make another gateway call.
        Every other gateway exception propagates as the same exception object.
        Custom gateways that mutate the supplied record are outside scope.

        ## Examples

        - Owner `" A "`, retries `0`: send `{"owner": "a", "retries": 0}` once.
        - Gateway returns `"job-8"`: return that exact receipt with status `"accepted"`.
        - Gateway raises `GatewayUnavailable`: return status `"retry"` with no receipt.
        - Gateway raises `ValueError`: propagate it. Do not return status `"retry"`.
        - Owner is `" "`: raise `ValueError` before any gateway call.

        ## Boundary checklist

        - An unexpected exception detects a catch that is too broad.
        - Mixed-case input and an unknown key detect an unprocessed gateway argument.
        - Exact call count detects a duplicate send.
        - Blank input and zero calls detect missing validation before a side effect.
        - The handled exception must produce the exact response without a hidden retry.

        ## Pytest lesson: fakes and patch lookup

        Keep each fake small. Give it a call list and a configured outcome.
        Use a fresh fake for each test so that call history cannot leak between tests.
        Use `pytest.raises` for an exception that must propagate.
        You can use `as caught` to inspect the exception object.

        Patching is another way to replace a dependency temporarily.
        Patch the name where the caller looks it up.
        For example, this service imports `prepare_payload` into `app.service`.
        Replacing `app.validation.prepare_payload` after that import would not
        replace the name already held by `app.service`.
        Its lookup name is `app.service.prepare_payload`.
        Keep that function real for this assignment. Constructor injection already
        gives you the gateway boundary without a patch.

        ## Commands

        Run from the new lab directory.

        ```sh
        uv run pytest -q tests/test_existing.py
        uv run pytest --collect-only -q tests/learner
        uv run pytest -q tests/learner
        uv run pytest -q tests/learner -k exception
        uv run pytest -q
        git diff -- app tests/learner
        ```

        Read new untracked files directly if they do not appear in `git diff`.

        ## Optional AI review

        "Review my fake and my tests. Cite the file and function for the real
        caller path. Check whether my tests preserve validation and test the
        exception boundary. Do not write code or tests. I will write all code."

        Constructed AI claim to check: "Catching every exception from send is
        safer because every gateway failure should become a retry response."

        ## Hints

        First, make a fake return a receipt that the source cannot predict.
        Next, record arguments before the fake returns or raises.
        Finally, use separate cases for a known outage and an unexpected adapter error.
        Do not infer the call count only from the returned response.

        ## Done checks

        The real service and validation run in every caller test.
        Success and both exception classes have explicit output or exception assertions.
        Invalid input has an explicit zero-call assertion.
        Correct code passes. Every supplied faulty variant fails by assertion.
        Passing fake-based tests does not verify a real external gateway.
    '''),
    "editable": ["tests/learner/"],
    "files": {
        "app/__init__.py": "",
        "app/errors.py": dedent('''\
            class GatewayUnavailable(RuntimeError):
                """The gateway cannot accept the record now."""
        '''),
        "app/validation.py": VALIDATION,
        "app/gateway.py": dedent('''\
            from typing import Protocol


            class Gateway(Protocol):
                def send(self, record: dict) -> str: ...


            class MemoryGateway:
                """Local demonstration adapter; no network or retries."""

                def __init__(self):
                    self.records: list[dict] = []

                def send(self, record: dict) -> str:
                    self.records.append(dict(record))
                    return f"receipt-{len(self.records)}"
        '''),
        "app/service.py": SERVICE,
        "tests/test_existing.py": dedent('''\
            from app.gateway import MemoryGateway
            from app.service import IntakeService


            def test_local_gateway_supported_path():
                gateway = MemoryGateway()
                response = IntakeService(gateway).submit({"owner": "iris", "retries": 1})
                assert response == {"status": "accepted", "owner": "iris", "receipt": "receipt-1"}
                assert gateway.records == [{"owner": "iris", "retries": 1}]
        '''),
        "tests/learner/test_task.py": '"""Write your own tests here."""\n',
    },
    "reference": {},
    "contract_tests": CONTRACT_TESTS,
    "reference_tests": REFERENCE_TESTS,
    "variants": [
        {
            "name": "all gateway exceptions become retry results",
            "files": {"app/service.py": SERVICE.replace(
                "except GatewayUnavailable:", "except Exception:",
            )},
        },
        {
            "name": "gateway receives the raw request",
            "files": {"app/service.py": SERVICE.replace(
                "self.gateway.send(record)", "self.gateway.send(payload)",
            )},
        },
        {
            "name": "successful record is sent twice",
            "files": {"app/service.py": SERVICE.replace(
                "            receipt = self.gateway.send(record)",
                "            self.gateway.send(record)\n            receipt = self.gateway.send(record)",
            )},
        },
        {
            "name": "blank owner reaches the gateway",
            "files": {"app/validation.py": VALIDATION.replace(
                "not isinstance(owner, str) or not owner.strip()", "not isinstance(owner, str)",
            )},
        },
    ],
    "ai_claim": "Catching every exception from send is safer because every gateway failure should become a retry response.",
    "ai_answer": "False. A fake gateway that raises ValueError('adapter bug') is a counterexample. The contract requires that same ValueError to propagate after one call. A broad except Exception hides it behind {'status': 'retry', 'owner': ...}. Only GatewayUnavailable represents the handled outage.",
    "sources": [
        "https://docs.pytest.org/en/stable/how-to/assert.html",
        "https://docs.pytest.org/en/stable/how-to/monkeypatch.html",
    ],
}
