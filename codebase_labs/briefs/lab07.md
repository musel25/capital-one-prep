# lab07: Test a paged client with a fake clock and transport

[Back to the ordered course guide](../README.md)

**Objective:** Write deterministic tests for exact dependency calls, retries, shared budgets, and stop conditions.

**Practice estimate:** 60 minutes.

Start a fresh attempt from the repository root:

```sh
uv run python scripts/codebase.py start lab07
```

Open the printed folder and follow its README. It includes the exact check command.

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

## Check the AI claim

This is a constructed example. Assess it with code and tests.

> Using the original timeout for each page preserves the overall budget because each request has a timeout.

## Official references

- [Documentation 1](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
- [Documentation 2](https://docs.python.org/3/library/unittest.mock.html#where-to-patch)
- [Documentation 3](https://docs.pytest.org/en/stable/how-to/parametrize.html)
