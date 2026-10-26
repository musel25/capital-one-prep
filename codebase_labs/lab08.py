"""Instructor data for reviewing a supplied client patch."""

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

STARTER = CLIENT.replace("if page.next_cursor is None:", "if not page.next_cursor:")

PUBLIC = dedent('''\
from app.client import collect
from app.types import Page, Result


def test_normal_nonempty_cursor():
    class Clock:
        def now_ms(self):
            return 90

        def wait_ms(self, duration):
            raise AssertionError("successful pages must not wait")

    class Transport:
        def __init__(self):
            self.calls = []

        def fetch(self, cursor, *, timeout_ms):
            self.calls.append((cursor, timeout_ms))
            if cursor is None:
                return Page(("a",), "next")
            return Page(("b",), None)

    remote = Transport()
    assert collect(remote, Clock(), budget_ms=9) == Result(("a", "b"), "complete", 2)
    assert remote.calls == [(None, 9), ("next", 9)]
''')

CONTRACT_TESTS = dedent('''\
import pytest

from app.client import collect
from app.types import HttpFailure, Page, Result


class TestClock:
    __test__ = False

    def __init__(self):
        self.time = 500
        self.waits = []

    def now_ms(self):
        return self.time

    def wait_ms(self, duration):
        self.waits.append(duration)
        self.time += duration


class ScriptedTransport:
    def __init__(self, clock, steps):
        self.clock = clock
        self.steps = list(steps)
        self.calls = []

    def fetch(self, cursor, *, timeout_ms):
        self.calls.append((cursor, timeout_ms))
        duration, value = self.steps.pop(0) if self.steps else (0, Page(("EXTRA",), None))
        self.clock.time += duration
        if isinstance(value, Exception):
            raise value
        return value


@pytest.mark.parametrize("cursor", ["", " ", "None", "0"])
def test_opaque_cursors_are_forwarded_exactly(cursor):
    clock = TestClock()
    remote = ScriptedTransport(clock, [(2, Page(("first",), cursor)), (1, Page(("last",), None))])
    assert collect(remote, clock, budget_ms=11) == Result(("first", "last"), "complete", 2)
    assert remote.calls == [(None, 11), (cursor, 9)]
    assert clock.waits == []


def test_empty_page_is_not_a_stop_signal():
    clock = TestClock()
    remote = ScriptedTransport(clock, [(1, Page((), "next")), (1, Page(("found",), None))])
    assert collect(remote, clock, budget_ms=8) == Result(("found",), "complete", 2)
    assert remote.calls == [(None, 8), ("next", 7)]


@pytest.mark.parametrize("cursor", ["", "repeated"])
def test_repeated_cursors_stop_before_another_request(cursor):
    clock = TestClock()
    remote = ScriptedTransport(clock, [(0, Page(("a",), cursor)), (0, Page(("b",), cursor))])
    assert collect(remote, clock, budget_ms=10) == Result(("a", "b"), "cursor_loop", 2)
    assert remote.calls == [(None, 10), (cursor, 10)]


def test_retry_uses_empty_cursor_and_one_budget():
    clock = TestClock()
    remote = ScriptedTransport(clock, [(1, Page(("a",), "")), (2, HttpFailure(503)), (1, Page(("b",), None))])
    assert collect(remote, clock, budget_ms=12) == Result(("a", "b"), "complete", 3)
    assert remote.calls == [(None, 12), ("", 11), ("", 7)]
    assert clock.waits == [2]


@pytest.mark.parametrize("page,limit,result", [
    (Page((), None), 1, Result((), "complete", 1)),
    (Page(("last",), None), 1, Result(("last",), "complete", 1)),
    (Page(("kept",), ""), 1, Result(("kept",), "page_limit", 1)),
])
def test_terminal_and_page_limit_precedence(page, limit, result):
    clock = TestClock()
    remote = ScriptedTransport(clock, [(0, page)])
    assert collect(remote, clock, budget_ms=10, max_pages=limit) == result
    assert remote.calls == [(None, 10)]


def test_zero_and_exhausted_budget_do_not_fetch():
    clock = TestClock()
    remote = ScriptedTransport(clock, [])
    assert collect(remote, clock, budget_ms=0) == Result((), "budget", 0)
    assert remote.calls == []
    remote = ScriptedTransport(clock, [(4, Page(("a",), ""))])
    assert collect(remote, clock, budget_ms=4) == Result(("a",), "budget", 1)
    assert remote.calls == [(None, 4)]


def test_retries_keep_existing_limits_and_delays():
    clock = TestClock()
    remote = ScriptedTransport(clock, [(1, HttpFailure(429)), (1, HttpFailure(503)), (0, HttpFailure(503))])
    assert collect(remote, clock, budget_ms=20) == Result((), "retry_limit", 3)
    assert remote.calls == [(None, 20), (None, 17), (None, 12)]
    assert clock.waits == [2, 4]


def test_fatal_error_and_unexpected_exception():
    clock = TestClock()
    remote = ScriptedTransport(clock, [(0, HttpFailure(500))])
    assert collect(remote, clock, budget_ms=8) == Result((), "fatal", 1)
    assert len(remote.calls) == 1
    assert clock.waits == []
    remote = ScriptedTransport(clock, [(0, RuntimeError("adapter"))])
    with pytest.raises(RuntimeError, match="adapter"):
        collect(remote, clock, budget_ms=8)


def test_insufficient_retry_time_does_not_wait():
    clock = TestClock()
    remote = ScriptedTransport(clock, [(4, HttpFailure(429))])
    assert collect(remote, clock, budget_ms=6) == Result((), "budget", 1)
    assert clock.waits == []


def test_attempt_limit_resets_and_duplicates_are_kept():
    clock = TestClock()
    remote = ScriptedTransport(clock, [(0, HttpFailure(503)), (0, Page(("a", "a"), "n")), (0, HttpFailure(429)), (0, Page(("a",), None))])
    assert collect(remote, clock, budget_ms=12, max_attempts=2) == Result(("a", "a", "a"), "complete", 4)
    assert clock.waits == [2, 2]


@pytest.mark.parametrize("options", [{"budget_ms": -1}, {"budget_ms": False}, {"budget_ms": 8, "max_attempts": 0}, {"budget_ms": 8, "max_pages": 1.0}])
def test_invalid_limits_reject_before_calls(options):
    clock = TestClock()
    remote = ScriptedTransport(clock, [])
    with pytest.raises(ValueError, match="invalid"):
        collect(remote, clock, **options)
    assert remote.calls == []
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
        return 77 + self.elapsed

    def wait_ms(self, duration):
        self.elapsed += duration
        self.waits.append(duration)


class FakeRemote:
    def __init__(self, clock, *steps):
        self.clock = clock
        self.steps = iter(steps)
        self.calls = []

    def fetch(self, cursor, *, timeout_ms):
        self.calls.append((cursor, timeout_ms))
        duration, answer = next(self.steps, (0, Page(("unexpected",), None)))
        self.clock.elapsed += duration
        if isinstance(answer, Exception):
            raise answer
        return answer


def test_empty_cursor_is_a_real_next_request():
    clock = FakeClock()
    remote = FakeRemote(clock, (3, Page(("A",), "")), (2, Page(("B",), None)))
    result = collect(remote, clock, budget_ms=15)
    assert result == Result(("A", "B"), "complete", 2)
    assert remote.calls == [(None, 15), ("", 12)]
    assert clock.waits == []


def test_empty_page_can_have_more_results():
    clock = FakeClock()
    remote = FakeRemote(clock, (0, Page((), "later")), (0, Page(("C",), None)))
    assert collect(remote, clock, budget_ms=7) == Result(("C",), "complete", 2)
    assert remote.calls == [(None, 7), ("later", 7)]


@pytest.mark.parametrize("token", ["", "same"])
def test_loop_detection_includes_empty_tokens(token):
    clock = FakeClock()
    remote = FakeRemote(clock, (1, Page(("A",), token)), (1, Page(("B",), token)))
    assert collect(remote, clock, budget_ms=9) == Result(("A", "B"), "cursor_loop", 2)
    assert remote.calls == [(None, 9), (token, 8)]


def test_empty_token_retries_keep_remaining_budget():
    clock = FakeClock()
    remote = FakeRemote(clock, (2, Page(("A",), "")), (1, HttpFailure(429)), (1, Page(("B",), None)))
    assert collect(remote, clock, budget_ms=20) == Result(("A", "B"), "complete", 3)
    assert remote.calls == [(None, 20), ("", 18), ("", 15)]
    assert clock.waits == [2]


def test_none_really_ends_and_page_limit_still_applies():
    clock = FakeClock()
    remote = FakeRemote(clock, (0, Page((), None)))
    assert collect(remote, clock, budget_ms=4, max_pages=1) == Result((), "complete", 1)
    assert remote.calls == [(None, 4)]
    remote = FakeRemote(clock, (0, Page(("kept",), "")))
    assert collect(remote, clock, budget_ms=4, max_pages=1) == Result(("kept",), "page_limit", 1)
    assert remote.calls == [(None, 4)]


def test_budget_end_with_empty_token_does_not_claim_completion():
    clock = FakeClock()
    remote = FakeRemote(clock, (5, Page(("A",), "")))
    assert collect(remote, clock, budget_ms=5) == Result(("A",), "budget", 1)
    assert remote.calls == [(None, 5)]


def test_fatal_and_retry_limits_remain_compatible():
    clock = FakeClock()
    remote = FakeRemote(clock, (0, HttpFailure(404)))
    assert collect(remote, clock, budget_ms=8) == Result((), "fatal", 1)
    assert clock.waits == []
    remote = FakeRemote(clock, (0, HttpFailure(503)), (0, HttpFailure(503)))
    assert collect(remote, clock, budget_ms=8, max_attempts=2) == Result((), "retry_limit", 2)
    assert remote.calls == [(None, 8), (None, 6)]
    assert clock.waits == [2]
''')

LAB = {
    "id": "lab08",
    "title": "Review an AI patch with an independent regression test",
    "kind": "repair",
    "after": 16,
    "minutes": 55,
    "objective": "Verify a supplied AI claim, reproduce one client regression, and repair it with a small diff.",
    "brief": dedent('''\
        # Context

        This is an independent snapshot of the constructed paged client.
        A supplied AI patch tries to make the completion check simpler.
        The patch is already applied. It causes one regression in cursor handling.
        Review the claim against the product rule. Write your own reproducing
        test before you repair the client. This is technical practice only.

        ## Learn first

        An opaque cursor is a token owned by the remote service.
        The caller forwards it without interpretation or normalization.
        This API reserves None as the end signal. Every string, including an
        empty string, can be a valid token.
        In Python, an empty string and None both have false truth values.
        A shorter condition can therefore change the set of accepted inputs.

        A regression is behavior that worked before a change and now fails.
        A useful regression test follows the public function and checks observable
        results. It does not search source text for a particular condition.
        Keep the real client. Inject a fake clock and transport.
        Record exact transport calls. A completion reason alone cannot prove
        that the client collected every required page.
        Reproduce the failure yourself before you ask AI to review your work.

        Worked trace: page one returns items `("A",)` and token `"next"`.
        Page two returns items `("B",)` and token None.
        With zero request duration and budget 10, calls are `(None, 10)` then
        `("next", 10)`. Result is `Result(("A", "B"), "complete", 2)`.
        Now apply the token rule to values that are absent from this example.

        ## Supplied patch and constructed AI claim

        This is a constructed example, not a real model transcript.
        The patch is in `app/client.py`:

        ```diff
        -        if page.next_cursor is None:
        +        if not page.next_cursor:
                     return Result(tuple(items), "complete", calls)
        ```

        Claim: "An empty cursor means there is no next page, so the shorter
        truth check preserves behavior and also handles empty cursors safely."
        Decide what evidence would falsify that claim before editing the code.

        ## File map

        - `app/__init__.py`: package marker.
        - `app/types.py`: Page, Result, and HttpFailure.
        - `app/contracts.py`: injected transport and clock interfaces.
        - `app/policy.py`: retryable statuses and delay calculation.
        - `app/client.py`: budget, retries, cursor forwarding, and stop conditions.
        - `tests/test_existing.py`: ordinary nonempty-cursor behavior.
        - `tests/learner/test_task.py`: your empty test file.

        ## Read and trace

        Run `rg -n 'next_cursor|seen|deadline|fetch' app`.
        Trace where a response token becomes the next request cursor.
        Find all conditions that can stop the client.
        Read the supplied diff as a behavior change, not a style improvement.
        Use the rule below to choose a counterexample with a distinct expected result.

        ## Assignment and allowed edits

        Write a failing regression under `tests/learner/` yourself.
        Assert the returned items and the exact cursor call sequence.
        Repair only the cursor regression in `app/client.py`.
        You may add more tests under `tests/learner/`.
        Do not change types, interfaces, policy, or public tests.
        Keep the repair small. Preserve the existing retry and budget behavior.
        Do not replace the client, redesign its result, or add network adapters.

        ## Exact accepted and rejected behavior

        `collect(transport, clock, budget_ms=..., max_attempts=3, max_pages=5)`
        returns `Result(items, reason, calls)`. Items is a tuple. Calls counts all
        fetches, including failures. Keep successful items in order, with duplicates.
        The first request cursor is None. Only a response cursor of None ends paging.
        Empty strings, whitespace strings, `"None"`, and `"0"` are valid tokens.
        Forward each token exactly. An empty item tuple is not an end signal.

        Add each successful page's items before checking stop conditions.
        Check these conditions in order: None gives `complete`; a next cursor
        already requested gives `cursor_loop`; max_pages with another cursor
        gives `page_limit`. Do not fetch a repeated cursor, including an empty one.
        A terminal page at max_pages still gives `complete`.

        Budget is one deadline for the full operation. Before each call, pass
        deadline minus current time as timeout_ms. If it is not positive, return
        `budget` with no additional call or wait. Request duration and waits both
        use this budget. A terminal response at the deadline is still complete.
        The transport must honor the timeout. Overruns and malformed pages are
        outside this model.

        Only HttpFailure 429 and 503 retry. Other statuses give `fatal`.
        Other exceptions propagate. Each page gets max_attempts, including its
        first call. Exhaustion gives `retry_limit`. Wait after failed attempt N is
        `2 * N` ms. If remaining time is less than or equal to the wait, return
        `budget` without waiting. Retry the identical cursor.
        Failed-call precedence is fatal, retry limit, then budget.
        Preserve earlier successful items on every stop.
        Budget must be an exact integer at least 0. max_attempts and max_pages
        must be exact integers at least 1. Invalid options raise ValueError before
        transport calls. Reject booleans and floats.

        ## Examples

        A page with `items=()` and `next_cursor="more"` still requires another call.
        Two successful pages can return the same item. Keep both copies.
        If a second page repeats the cursor used to request it, return cursor_loop
        after adding that page's items. Do not make a third call.
        A 429 error after 1 ms, with 8 ms initially remaining, permits a 2 ms wait.
        The retry receives timeout 5 and the same cursor.

        ## Boundary checklist

        - Empty string followed by a terminal page: detect the seeded AI regression.
        - Empty items with a nonterminal token: detect a false completion shortcut.
        - A repeated empty token: detect loop checks that skip false values.
        - None and ordinary tokens: preserve existing successful behavior.
        - Retry on an empty token: preserve the token and shared budget.
        - Empty token at the page or time limit: report the limit, not completion.
        - Fatal status and attempt exhaustion: preserve stop behavior.

        ## Focused commands and pytest techniques

        Run from the attempt directory. No running server is needed.
        Run `uv run pytest --collect-only -q tests/learner`.
        Run `uv run pytest -q tests/learner` before the repair.
        Read the assertion mismatch. Confirm that it matches your predicted failure.
        Run the same command after the repair. Then run `uv run pytest -q`.
        Use `@pytest.mark.parametrize` for related cursor classes.
        Give your fake a controlled extra-call response. Assert its call history,
        so an unexpected extra request fails an assertion rather than setup.
        Use `git diff -- app/client.py tests/learner` if files are tracked.
        Otherwise compare saved files with `git diff --no-index OLD NEW`.

        ## Optional AI review prompt

        "Review my regression test and small diff against the cursor contract.
        Cite the function and branch for your conclusions. Check one adjacent
        stop condition. Do not write tests or implementation. Do not redesign the
        client. State which behavior my evidence does not cover."

        ## Hints

        1. A token's truth value is not its protocol meaning.
        2. Test calls as well as returned items to detect early completion.
        3. Keep loop detection and page limits independent from token truthiness.

        ## Technical done checks

        Your test reproduces the supplied patch's failure through a normal assertion.
        Your repaired code passes that test and the public tests.
        Your tests also check an adjacent stop condition and retry compatibility.
        Review the small diff. Run the guide's local checker against this attempt.
        Passing tests support specific behavior claims. They do not prove readiness.
        This model excludes live networking, concurrency, cancellation, and storage.
        Official references: [pytest parameters](https://docs.pytest.org/en/stable/how-to/parametrize.html)
        and [Python truth values](https://docs.python.org/3/library/stdtypes.html#truth-value-testing).
        '''),
    "editable": ["app/client.py", "tests/learner/"],
    "files": {
        "app/__init__.py": "",
        "app/types.py": TYPES,
        "app/contracts.py": CONTRACTS,
        "app/policy.py": POLICY,
        "app/client.py": STARTER,
        "tests/test_existing.py": PUBLIC,
        "tests/learner/test_task.py": '"""Write your own tests here."""\n',
    },
    "reference": {"app/client.py": CLIENT},
    "contract_tests": CONTRACT_TESTS,
    "reference_tests": REFERENCE_TESTS,
    "variants": [
        {"name": "treats the empty cursor as terminal", "files": {"app/client.py": STARTER}},
        {"name": "treats empty items as terminal", "files": {"app/client.py": CLIENT.replace(
            "if page.next_cursor is None:", "if page.next_cursor is None or not page.items:"
        )}},
        {"name": "skips loop checks for empty cursors", "files": {"app/client.py": CLIENT.replace(
            "if page.next_cursor in seen:", "if page.next_cursor and page.next_cursor in seen:"
        )}},
    ],
    "ai_claim": "An empty cursor means there is no next page, so a truth check preserves behavior.",
    "ai_answer": "False. Page(('A',), '') followed by Page(('B',), None) must request cursors [None, ''] and return items ('A', 'B') with two calls. The supplied patch returns only ('A',) after one call. The protocol reserves None alone as the end signal.",
    "sources": [
        "https://docs.pytest.org/en/stable/how-to/parametrize.html",
        "https://docs.python.org/3/library/stdtypes.html#truth-value-testing",
    ],
}

