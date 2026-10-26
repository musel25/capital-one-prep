# Independent course review — 2026-10-26

No unresolved critical or important issue was found in the final source review.
This review covered all 50 authored problems, the builder, the verifier, and the
shared JSON marker code. It compared each contract with the Python reference,
the Java implementation, the explicit cases, and the mutation.

## Findings and corrections

- **Shared marker: invalid JSON Unicode escapes.** `Support.java` previously
  accepted `\u+041` because `Integer.parseInt` accepts a sign. For problem 04,
  a ticket with ID `A` caused the marker to accept the invalid output
  `["\u+041"]`. The marker now requires four ASCII hexadecimal digits. The
  focused regression passed: `uv run pytest -q tests/test_cojudge.py -k
  signed_unicode` reported **1 passed, 6 deselected**. This corrects a marker
  defect, not a learner exercise.
- **Problem 06: missing CSV size limits.** The previous contract allowed an
  account field with 131,073 characters. The Python reference raised
  `field larger than field limit (131072)` for that input. The final contract
  limits decoded account fields to 1,000 characters, amount fields to 20
  characters, and complete CSV text to 200,000 characters. New independent
  cases at the field limits passed in both languages.
- **Problem 02: amount format width.** The coordinator found that the stated
  12-digit integer-part limit was not enforced. The final implementations use
  a 1–12 digit limit. Independent checks accepted 12 zero digits and rejected
  13 zero digits, including a signed amount with a fractional part.

## Independent checks

These checks supplemented the course verifier. Expected values for the new
cases were specified independently of either reference implementation.
The reviewer entered these values from the contracts and direct arithmetic.
Some repeated inputs and expected lists use simple range expressions. Neither
reference supplied their expected results. The 51 cases are retained in
[`authoring/review-cases.json`](authoring/review-cases.json).
They are separate from the 1,515 official cases. None repeats an official input.

| Check | Result |
| --- | --- |
| Source contracts and implementations | All 50 reviewed |
| New cases checked against Python and compiled Java | 51 passed across all 50 problems |
| Mutations with a wrong-result witness from an explicit case | 51 of 51 |
| Faulty starters run without an exception and shown to give a wrong result | 11, 12, 17, 32, 36 |
| Final source validation | 50 specifications; 1,515 official cases: 655 explicit and 860 additional |
| Separate reviewer cases | 51 cases; not added to the official case set |
| Signed Unicode-escape regression | Passed |

Each mutation witness produced a different output. A syntax error or runtime
exception was not needed to reject any mutation. Witnesses included shared
dataclass lists, partial balance writes, lost LEFT JOIN rows, duplicate money
effects, stale receipt tokens, and wrong expiry boundaries.

The 51 new cases included these boundaries and combinations:

- Maximum integer batches, very large permitted integers, strict money text,
  Unicode identifiers, CSV quoting, embedded control characters, field limits,
  and UTC year changes with minute offsets.
- Nested copy isolation, large fee rounding, cumulative deposits and refunds,
  self-transfers, rejected batches, and the stated policy for failed event IDs.
- Exact route matching, method-check order, malformed field shapes, response
  snapshots, idempotency keys with control characters, cursor tuple order,
  maximum retry counts, deadlines, and cache validators after a version increase.
- SQL value binding, significant spaces and quotes, NULL values, duplicate
  display names, a 300-row aggregate of 300,000,000, ranking before the cutoff,
  and rollback with embedded NUL characters in permitted IDs.
- Cache replacement, receipt versions, failed recovery probes, blocked jobs
  downstream from a cycle, reused hash-ring points, negative replica values,
  reservation expiry before conflict checks, and payment rollback plus replay.

Examples of independently specified numeric results were:

- Problem 01: 100 accepted values of 1,000,000,000 give 100,000,000,000.
- Problem 15: 999,999,999,999 cents at 9,999 basis points give a rounded fee of
  999,900,000,000 cents and a total of 1,999,899,999,999 cents.
- Problem 33: 300 paid rows of 1,000,000 give 300 events, 300 valued rows,
  and a total of 300,000,000 at both inclusive thresholds.
- Problem 36: transfers from 99 accounts, each with 1,000,000, into the remaining
  account produce 100,000,000 there and zero in every other account.

All fields used for string ordering in problems 41–50 are restricted to ASCII.
Java UTF-16 ordering and Python code-point ordering therefore agree in those
contracts. The new cases also checked that permitted control characters remain
distinct keys in SQL and API state.

## Teaching scope and limits

The course teaches typed boundaries, dataclasses, inheritance, composition,
API policy, SQLite queries, transactions, and small system components. The
lessons explain the concept before the task. The five faulty starters above
provide runnable defects. The other starters leave the required behavior for
the learner to implement.

The explicit cases cover different behaviors. Some additional cases vary
parameters within one pattern. Those cases add coverage, but their count alone
does not prove test diversity. One rejected mutation per problem is a useful
minimum; it does not prove that every realistic wrong solution will fail.

The statements identify constructed exercises and state the relevant limits.
The output judge cannot certify typing, inheritance, SQL use, data structures,
or time complexity. SQL references execute actual SQLite statements. API,
queue, cache, and distributed-system tasks use sequential state simulations.
They do not test live services, real parallel execution, durable recovery,
security, or complete system design. Course completion does not prove interview
readiness.

This review did not test deployment, browser behavior, or live judge execution.
The coordinator performs those checks separately. No learner attempt or private
behavioral note was read or changed. This reviewer wrote this report and the
separate reviewer case artifact. No other repository file was changed by this
reviewer. No commit was made.
