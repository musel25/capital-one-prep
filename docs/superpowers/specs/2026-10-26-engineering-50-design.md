# Capital One Engineering 50

The user wants 50 original, progressive, technical-only problems on
https://cojudge.musel.dev. Basic LeetCode is already familiar. Short tasks,
clear lessons, diverse tests, and production failure cases are the priority.

Use the existing CoJudge custom-content mechanism. Keep the source pack in
this repository under `cojudge/`. Publish only its `problems/` and `courses/`
directories to the existing server content volume. Do not modify upstream
CoJudge, existing courses, learner attempts, or saved browser progress.

Five ordered levels contain ten problems each:

1. Python data boundaries and standard libraries (01–10).
2. Objects, state, and business rules (11–20).
3. API behavior and reliable clients (21–30).
4. SQL and database correctness (31–40).
5. Small system components and integration (41–50).

Python is the learner language. Use its standard library and Python 3.11
compatible code because that is the installed judge runtime. Run local
Python with `uv run`. SQL solutions use an actual in-memory SQLite database.
Network and concurrent operations are deterministic simulations; never
claim they are live services or tests of real parallel execution.

Each problem has one short lesson, a precise contract, two or three examples,
constraints, prerequisites, estimated practice time, hints, starter code,
an optional reference solution, and diverse official tests. The lesson
teaches the new concept before the task. There is no behavioral practice.

Use CoJudge's supported string input/output with a supplied JSON adapter.
The learner implements `solve(data)` using normal Python values. The adapter
must not require manual JSON escaping. Statements show decoded inputs.
Java markers compute answers for arbitrary valid inputs, including custom
tests. They compare parsed JSON structurally, ignoring object key order and
whitespace while preserving list order and distinguishing booleans/numbers.

At least 12 distinct hand-checked cases and 12 deterministic additional cases
per problem. Verify all explicit expected values against Python and Java.
Include at least one realistic wrong implementation per problem; the tests
must reject it. Include several runnable bug-fix starters. Markers must also
reject wrong types, altered outputs, and invalid JSON.

Typing, inheritance, SQL use, and complexity cannot be certified by an output
judge. State this limitation clearly. Reference code demonstrates the stated
technique. Do not promise comprehensive interview coverage or readiness.
Original constructed exercises must be distinguished from employer material.

Builder choices: specific task titles and bounded contracts, helper code,
test generation, source pack layout, and deployment scripts. The user has
authorized creation and publication to the existing website.
