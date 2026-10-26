"""Instructor data for deterministic paged-client tests."""

from textwrap import dedent


TYPES = dedent('''\
from dataclasses import dataclass


@dataclass(frozen=True)
class Page:
    items: tuple[str, ...]
    next_cursor: str | None


@dataclass(frozen=True)
class Result:
    items: tuple[str, ...]
    reason: str
    calls: int


class HttpFailure(Exception):
    def __init__(self, status):
        self.status = status
        super().__init__(f"HTTP {status}")
''')

CONTRACTS = dedent('''\
from typing import Protocol

from app.types import Page


class Transport(Protocol):
    def fetch(self, cursor: str | None, *, timeout_ms: int) -> Page: ...


class Clock(Protocol):
    def now_ms(self) -> int: ...
    def wait_ms(self, duration: int) -> None: ...
''')

POLICY = dedent('''\
def is_retryable(status):
    return status in (429, 503)


def retry_delay(failed_attempt):
    return 2 * failed_attempt
''')

CLIENT = dedent('''\
from app.contracts import Clock, Transport
from app.policy import is_retryable, retry_delay
from app.types import HttpFailure, Result


def collect(transport: Transport, clock: Clock, *, budget_ms, max_attempts=3, max_pages=5):
    for name, value, minimum in (
        ("budget_ms", budget_ms, 0),
        ("max_attempts", max_attempts, 1),
        ("max_pages", max_pages, 1),
    ):
        if type(value) is not int or value < minimum:
            raise ValueError(f"invalid {name}")
    deadline = clock.now_ms() + budget_ms
    cursor = None
    seen = {None}
    items = []
    calls = 0
    pages = 0
    while True:
        attempt = 0
        while True:
            remaining = deadline - clock.now_ms()
            if remaining <= 0:
                return Result(tuple(items), "budget", calls)
            attempt += 1
            calls += 1
            try:
                page = transport.fetch(cursor, timeout_ms=remaining)
            except HttpFailure as error:
                if not is_retryable(error.status):
                    return Result(tuple(items), "fatal", calls)
                if attempt >= max_attempts:
                    return Result(tuple(items), "retry_limit", calls)
                delay = retry_delay(attempt)
                if deadline - clock.now_ms() <= delay:
                    return Result(tuple(items), "budget", calls)
                clock.wait_ms(delay)
                continue
            break
        pages += 1
        items.extend(page.items)
        if page.next_cursor is None:
            return Result(tuple(items), "complete", calls)
        if page.next_cursor in seen:
            return Result(tuple(items), "cursor_loop", calls)
        if pages >= max_pages:
            return Result(tuple(items), "page_limit", calls)
        seen.add(page.next_cursor)
        cursor = page.next_cursor
''')

PUBLIC = dedent('''\
from app.client import collect
from app.types import Page, Result


def test_one_page_completes_without_waiting():
    class Clock:
        def now_ms(self):
            return 100

        def wait_ms(self, duration):
            raise AssertionError("a successful page must not wait")

    class Transport:
        def fetch(self, cursor, *, timeout_ms):
            assert cursor is None
            assert timeout_ms == 10
            return Page(("ticket-1",), None)

    assert collect(Transport(), Clock(), budget_ms=10) == Result(("ticket-1",), "complete", 1)
''')

CONTRACT_TESTS = dedent('''\
import pytest

from app.client import collect
from app.types import HttpFailure, Page, Result


class VirtualClock:
    def __init__(self):
        self.time = 200
        self.waits = []

    def now_ms(self):
        return self.time

    def wait_ms(self, duration):
        self.waits.append(duration)
        self.time += duration


class Script:
    def __init__(self, clock, entries):
        self.clock = clock
        self.entries = list(entries)
        self.calls = []

    def fetch(self, cursor, *, timeout_ms):
        self.calls.append((cursor, timeout_ms))
        spent, answer = self.entries.pop(0) if self.entries else (0, Page(("EXTRA",), None))
        self.clock.time += spent
        if isinstance(answer, Exception):
            raise answer
        return answer


def test_one_deadline_across_pages_and_preserved_order():
    clock = VirtualClock()
    transport = Script(clock, [(5, Page(("a", "a"), "next")), (3, Page(("b",), None))])
    assert collect(transport, clock, budget_ms=20) == Result(("a", "a", "b"), "complete", 2)
    assert transport.calls == [(None, 20), ("next", 15)]
    assert clock.waits == []


def test_retry_attempt_limit_resets_for_each_page():
    clock = VirtualClock()
    transport = Script(clock, [
        (1, HttpFailure(503)), (1, Page(("a",), "n")),
        (1, HttpFailure(429)), (1, Page(("b",), None)),
    ])
    assert collect(transport, clock, budget_ms=20, max_attempts=2) == Result(("a", "b"), "complete", 4)
    assert transport.calls == [(None, 20), (None, 17), ("n", 16), ("n", 13)]
    assert clock.waits == [2, 2]


@pytest.mark.parametrize("status", [400, 401, 404, 500])
def test_non_retryable_failure_stops_and_keeps_prior_items(status):
    clock = VirtualClock()
    transport = Script(clock, [(1, Page(("kept",), "n")), (1, HttpFailure(status))])
    assert collect(transport, clock, budget_ms=10) == Result(("kept",), "fatal", 2)
    assert transport.calls == [(None, 10), ("n", 9)]
    assert clock.waits == []


def test_equal_wait_and_remaining_budget_does_not_wait():
    clock = VirtualClock()
    transport = Script(clock, [(3, HttpFailure(429))])
    assert collect(transport, clock, budget_ms=5) == Result((), "budget", 1)
    assert transport.calls == [(None, 5)]
    assert clock.waits == []
    assert clock.time == 203


def test_attempts_include_initial_call_and_last_failure_has_no_wait():
    clock = VirtualClock()
    transport = Script(clock, [(1, HttpFailure(503))] * 3)
    assert collect(transport, clock, budget_ms=30, max_attempts=3) == Result((), "retry_limit", 3)
    assert transport.calls == [(None, 30), (None, 27), (None, 22)]
    assert clock.waits == [2, 4]


def test_zero_budget_has_no_side_effects():
    clock = VirtualClock()
    transport = Script(clock, [])
    assert collect(transport, clock, budget_ms=0) == Result((), "budget", 0)
    assert transport.calls == []
    assert clock.waits == []


@pytest.mark.parametrize("entries,limit,expected,calls", [
    ([(0, Page((), "")), (0, Page(("b",), None))], 5, Result(("b",), "complete", 2), [(None, 10), ("", 10)]),
    ([(0, Page(("a",), "x")), (0, Page(("b",), "x"))], 5, Result(("a", "b"), "cursor_loop", 2), [(None, 10), ("x", 10)]),
    ([(0, Page(("a",), "x"))], 1, Result(("a",), "page_limit", 1), [(None, 10)]),
    ([(10, Page(("a",), None))], 1, Result(("a",), "complete", 1), [(None, 10)]),
    ([(10, Page(("a",), "x"))], 5, Result(("a",), "budget", 1), [(None, 10)]),
])
def test_pagination_stop_conditions(entries, limit, expected, calls):
    clock = VirtualClock()
    transport = Script(clock, entries)
    assert collect(transport, clock, budget_ms=10, max_pages=limit) == expected
    assert transport.calls == calls


@pytest.mark.parametrize("options", [{"budget_ms": -1}, {"budget_ms": True}, {"budget_ms": 3.0}, {"budget_ms": 5, "max_attempts": 0}, {"budget_ms": 5, "max_pages": False}])
def test_bad_configuration_fails_before_transport(options):
    clock = VirtualClock()
    transport = Script(clock, [])
    with pytest.raises(ValueError, match="invalid"):
        collect(transport, clock, **options)
    assert transport.calls == []


def test_unexpected_transport_exception_propagates():
    clock = VirtualClock()
    transport = Script(clock, [(0, RuntimeError("broken adapter"))])
    with pytest.raises(RuntimeError, match="broken adapter"):
        collect(transport, clock, budget_ms=8)
    assert clock.waits == []
''')

REFERENCE_TESTS = dedent('''\
import pytest

from app.client import collect
from app.types import HttpFailure, Page, Result


class FakeClock:
    def __init__(self):
        self.elapsed = 0
        self.waits = []

    def now_ms(self):
        return 1000 + self.elapsed

    def wait_ms(self, duration):
        self.waits.append(duration)
        self.elapsed += duration


class FakeTransport:
    def __init__(self, clock, *steps):
        self.clock = clock
        self.steps = iter(steps)
        self.calls = []

    def fetch(self, cursor, *, timeout_ms):
        self.calls.append((cursor, timeout_ms))
        duration, value = next(self.steps, (0, Page(("unexpected",), None)))
        self.clock.elapsed += duration
        if isinstance(value, Exception):
            raise value
        return value


def test_shared_budget_and_retry_cursor_with_a_new_page():
    clock = FakeClock()
    remote = FakeTransport(clock, (4, Page(("first",), "p2")), (2, HttpFailure(503)), (3, Page(("second",), None)))
    assert collect(remote, clock, budget_ms=30) == Result(("first", "second"), "complete", 3)
    assert remote.calls == [(None, 30), ("p2", 26), ("p2", 22)]
    assert clock.waits == [2]
    assert clock.elapsed == 11


def test_each_page_gets_its_own_attempt_count():
    clock = FakeClock()
    remote = FakeTransport(clock, (0, HttpFailure(429)), (0, Page(("x",), "n")), (0, HttpFailure(503)), (0, Page(("y",), None)))
    result = collect(remote, clock, budget_ms=15, max_attempts=2)
    assert result == Result(("x", "y"), "complete", 4)
    assert remote.calls == [(None, 15), (None, 13), ("n", 13), ("n", 11)]
    assert clock.waits == [2, 2]


@pytest.mark.parametrize("status", [400, 404, 500])
def test_fatal_errors_do_not_retry(status):
    clock = FakeClock()
    remote = FakeTransport(clock, (0, HttpFailure(status)))
    assert collect(remote, clock, budget_ms=40) == Result((), "fatal", 1)
    assert remote.calls == [(None, 40)]
    assert clock.waits == []


@pytest.mark.parametrize("budget,duration", [(2, 0), (7, 5)])
def test_no_wait_when_it_would_consume_all_time(budget, duration):
    clock = FakeClock()
    remote = FakeTransport(clock, (duration, HttpFailure(503)))
    assert collect(remote, clock, budget_ms=budget) == Result((), "budget", 1)
    assert clock.waits == []
    assert remote.calls == [(None, budget)]


def test_retry_limit_and_backoff_are_exact():
    clock = FakeClock()
    remote = FakeTransport(clock, (0, HttpFailure(503)), (0, HttpFailure(503)), (0, HttpFailure(503)))
    assert collect(remote, clock, budget_ms=20) == Result((), "retry_limit", 3)
    assert remote.calls == [(None, 20), (None, 18), (None, 14)]
    assert clock.waits == [2, 4]


def test_empty_cursor_and_empty_page_are_not_terminal():
    clock = FakeClock()
    remote = FakeTransport(clock, (0, Page((), "")), (0, Page(("a", "a"), None)))
    assert collect(remote, clock, budget_ms=4) == Result(("a", "a"), "complete", 2)
    assert remote.calls == [(None, 4), ("", 4)]


def test_limits_stop_before_extra_calls_and_keep_collected_items():
    clock = FakeClock()
    remote = FakeTransport(clock, (1, Page(("a",), "next")))
    assert collect(remote, clock, budget_ms=8, max_pages=1) == Result(("a",), "page_limit", 1)
    assert remote.calls == [(None, 8)]
    clock = FakeClock()
    remote = FakeTransport(clock, (0, Page(("a",), "same")), (0, Page(("b",), "same")))
    assert collect(remote, clock, budget_ms=8) == Result(("a", "b"), "cursor_loop", 2)
    assert len(remote.calls) == 2
    clock = FakeClock()
    remote = FakeTransport(clock)
    assert collect(remote, clock, budget_ms=0) == Result((), "budget", 0)
    assert remote.calls == []


def test_programming_errors_are_not_network_errors():
    clock = FakeClock()
    remote = FakeTransport(clock, (0, RuntimeError("bad fake")))
    with pytest.raises(RuntimeError, match="bad fake"):
        collect(remote, clock, budget_ms=5)
''')

LAB = {
    "id": "lab07",
    "title": "Test a paged client with a fake clock and transport",
    "kind": "tests",
    "after": 16,
    "minutes": 60,
    "objective": "Write deterministic tests for exact dependency calls, retries, shared budgets, and stop conditions.",
    "brief": dedent('''\
        # Context

        This constructed client collects ticket IDs from pages.
        It must stop within a shared time budget. It retries only selected errors.
        The application is correct in this snapshot. Your assignment is to write
        tests that can detect plausible client regressions.
        Keep the client real. Replace its transport and clock with your own fakes.

        ## Learn first

        A dependency is a collaborator that a function uses.
        Dependency injection means passing that collaborator into the function.
        A fake is a small test implementation with controlled behavior.
        This client receives both dependencies as arguments to `collect`.
        `Transport.fetch(cursor, timeout_ms=...)` returns a `Page` or raises an error.
        `Clock.now_ms()` reads virtual time. `Clock.wait_ms(duration)` advances it.
        Build a fake clock with an integer counter and a list of waits.
        Let the fake transport advance that same counter for request duration.
        Record each `(cursor, timeout_ms)` call before returning its scripted value.
        Do not call a network service or use real sleep.

        A deadline is the fixed finish time for the whole collection.
        Remaining time equals deadline minus current time.
        Worked trace: start at 100 with budget 12. The first call receives timeout
        12 and fails with 503 after 3 ms. The first retry delay is 2 ms.
        Time is now 105, so the next call receives timeout 7, with the same cursor.
        A later page uses the same deadline, 112.

        Use `assert` for returned values and exact call lists.
        Use `pytest.raises` for errors that must propagate.
        Use parameters to group error status classes with the same rule.
        Make a new fake clock and transport for each test to avoid state leakage.
        A line can execute without its boundary rule being tested. Coverage alone
        does not prove that your assertions detect a wrong timeout or extra call.

        ## File map

        - `app/__init__.py`: package marker.
        - `app/types.py`: Page, Result, and HttpFailure.
        - `app/contracts.py`: dependency interfaces described with Protocol.
        - `app/policy.py`: retry classification and delay calculation.
        - `app/client.py`: page loop, retry loop, budget, and stopping rules.
        - `tests/test_existing.py`: one supported page and basic fake syntax.
        - `tests/learner/test_task.py`: your empty test file.

        ## Read and trace

        Run `rg -n 'deadline|attempt|fetch|return Result' app`.
        Locate the loop for pages and the loop for attempts on one page.
        Trace one failure, one retry, and the transition to the next page.
        Calculate all timeouts on paper before running your first budget test.

        ## Assignment and allowed edits

        Write all tests yourself under `tests/learner/`.
        Do not change application files or public tests.
        Exercise the real `collect` function with your fake dependencies.
        Check output, reason, call count, exact call arguments, and wait history.
        Give the fake a controlled fallback for unexpected extra calls so that
        an extra call produces a useful assertion failure instead of IndexError.

        ## Exact accepted and rejected behavior

        Call `collect(transport, clock, budget_ms=..., max_attempts=3, max_pages=5)`.
        All three options must be exact integers. Reject booleans and floats.
        Budget must be at least 0. The other limits must be at least 1.
        Invalid options raise ValueError before any transport call.
        Result fields are `items` (tuple), `reason` (string), and `calls` (integer).
        Returned items include all successful pages in order. Keep duplicates.

        The first cursor is None. Each successful page supplies the next cursor.
        Only `next_cursor is None` means complete. An empty string is a valid
        opaque cursor. Do not interpret or change it. Empty items do not end paging.
        Add the page's items before evaluating its stopping condition.
        After a successful page, stop in this order: terminal None gives `complete`;
        a next cursor already requested gives `cursor_loop`; reaching max_pages
        with another cursor gives `page_limit`. Never fetch the repeated cursor.
        A terminal page at max_pages still gives `complete`.

        Before every fetch, calculate remaining time from one shared deadline.
        If it is zero or negative, return `budget` without a call or wait.
        Pass the entire positive remainder as the fetch timeout.
        Request duration and retry waits both consume the same budget.
        A successful terminal response at the deadline is still complete.
        A transport must honor its timeout. Malformed pages and overrunning
        transports are outside this model.

        Only HttpFailure statuses 429 and 503 can retry. Other statuses return
        `fatal`. Other exception types propagate unchanged.
        Count the initial call as attempt 1. Reset attempts for each new page.
        At max_attempts, return `retry_limit` without another wait or call.
        Otherwise the wait after failed attempt N is `2 * N` milliseconds.
        If remaining time is less than or equal to that wait, return `budget`
        immediately. Do not wait unless some time remains for a later request.
        Retry the same cursor. Count each fetch, including failures, in calls.
        Keep all earlier successful items on every stop.
        On a failed call, precedence is fatal, retry limit, then budget.

        ## Examples

        Budget 20, first page takes 5 ms, second takes 3 ms:
        call timeouts are 20 and 15. There are no waits.
        Budget 5, first 429 takes 3 ms: remaining 2 equals the wait 2.
        Return `Result((), "budget", 1)` with no waits.
        With max_attempts 2, a 503 then success can occur on each of two pages.
        There are four calls and two waits of 2 ms.

        ## Boundary checklist

        - Time spent before the next page: detect a reset global deadline.
        - A retry on each of two pages: detect a shared attempt counter.
        - 400, 404, and 500: detect retries of fatal errors.
        - Remaining time exactly equal to delay: detect a useless final wait.
        - Two retry failures: check delays 2 then 4 and exact remaining budgets.
        - Initial zero budget and final attempt: prove no extra calls or waits.
        - None, empty cursor, empty page, repeated cursor, and page limit:
          check stop conditions and retained items.
        - Duplicate IDs: preserve order without deduplication.

        ## Focused commands and pytest techniques

        Run from the attempt directory. No server or network setup is needed.
        Run `uv run pytest --collect-only -q tests/learner`.
        Run `uv run pytest -q tests/learner`.
        Run `uv run pytest -q` for all tests.
        Use `uv run pytest -q tests/learner -k budget` to isolate a named case.
        Start with an exact call-list assertion; compare its first differing tuple.
        Use `git diff -- tests/learner` when files are tracked.

        Injection is sufficient here. If you later patch an imported helper, patch
        where the caller looks it up. `client.py` imports `is_retryable` directly,
        so that lookup is `app.client.is_retryable`, not `app.policy.is_retryable`.
        Do not patch collect itself or the rule that your test needs to verify.

        ## Optional AI review prompt

        "Read my tests and the client. Cite the code path for each expected
        timeout. Find one missing boundary or weak assertion. Do not write the
        test, replace the client, or calculate all expected values for me."

        Constructed AI claim to check: "Giving each page the original timeout
        preserves the overall budget because each request has a timeout."

        ## Hints

        1. Record both call arguments and waits. A correct result can hide extra work.
        2. Use a starting clock value other than zero to test relative time.
        3. A successful page and a failed attempt affect different counters.

        ## Technical done checks

        Your tests collect and pass against this correct application.
        They use no network, real sleep, or clock-dependent values.
        Each expected timeout is calculated from the stated rule.
        Run the guide's local checker. Review which faulty behavior each test detects.
        This is a synchronous model. It excludes cancellation, parallel requests,
        Retry-After headers, malformed pages, and persistence.
        Official references: [pytest monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
        and [where to patch](https://docs.python.org/3/library/unittest.mock.html#where-to-patch).
        '''),
    "editable": ["tests/learner/"],
    "files": {
        "app/__init__.py": "",
        "app/types.py": TYPES,
        "app/contracts.py": CONTRACTS,
        "app/policy.py": POLICY,
        "app/client.py": CLIENT,
        "tests/test_existing.py": PUBLIC,
        "tests/learner/test_task.py": '"""Write your own tests here."""\n',
    },
    "reference": {},
    "contract_tests": CONTRACT_TESTS,
    "reference_tests": REFERENCE_TESTS,
    "variants": [
        {"name": "resets the budget on each page", "files": {"app/client.py": CLIENT.replace(
            "        cursor = page.next_cursor", "        cursor = page.next_cursor\n        deadline = clock.now_ms() + budget_ms"
        )}},
        {"name": "shares attempts across pages", "files": {"app/client.py": CLIENT.replace(
            "    while True:\n        attempt = 0\n", "    attempt = 0\n    while True:\n"
        )}},
        {"name": "retries fatal statuses", "files": {"app/client.py": CLIENT.replace(
            "if not is_retryable(error.status):", "if error.status < 400:"
        )}},
        {"name": "waits when no request time remains", "files": {"app/client.py": CLIENT.replace(
            "if deadline - clock.now_ms() <= delay:", "if deadline - clock.now_ms() < delay:"
        )}},
    ],
    "ai_claim": "Using the original timeout for each page preserves the overall budget because each request has a timeout.",
    "ai_answer": "False. Start with budget 20 ms. If page one takes 5 ms, page two may receive only 15 ms. Resetting it to 20 permits the whole operation to take 25 ms. Per-request timeouts do not establish one shared deadline.",
    "sources": [
        "https://docs.pytest.org/en/stable/how-to/monkeypatch.html",
        "https://docs.python.org/3/library/unittest.mock.html#where-to-patch",
        "https://docs.pytest.org/en/stable/how-to/parametrize.html",
    ],
}
