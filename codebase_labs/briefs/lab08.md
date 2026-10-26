# lab08: Review an AI patch with an independent regression test

[Back to the ordered course guide](../README.md)

**Objective:** Verify a supplied AI claim, reproduce one client regression, and repair it with a small diff.

**Practice estimate:** 55 minutes.

Start a fresh attempt from the repository root:

```sh
uv run python scripts/codebase.py start lab08
```

Open the printed folder and follow its README. It includes the exact check command.

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

## Check the AI claim

This is a constructed example. Assess it with code and tests.

> An empty cursor means there is no next page, so a truth check preserves behavior.

## Official references

- [Documentation 1](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [Documentation 2](https://docs.python.org/3/library/stdtypes.html#truth-value-testing)
