# Capital One Engineering 50

[Open the course](https://cojudge.musel.dev/?course=capital-one-engineering-50).

This is a technical-only course for a learner who knows basic LeetCode.
These are original constructed exercises. They are not official Capital One
questions. Completing them does not certify interview readiness.

## Start with one problem

1. Open problem 01.
2. Select **Python** in the editor.
3. Read **Learn first**.
4. Implement the small `solve(data)` task.
5. Use **Run** to check the examples.
6. Use **Submit** to check all official cases.
7. Open one hint if you are stuck.

The reference solution is optional. Each problem is independent, so a mistake
in an earlier solution cannot break a later problem. The skills build on each
other. Estimated times are guides, not deadlines. Start with the first level.

## Skill map

| Problems | Focus | What you practice |
| --- | --- | --- |
| 01–10 | Python data and libraries | Strict validation, exact money, missing values, stable order, counts, CSV, typed JSON, UTC, iterators, heaps |
| 11–20 | Objects and state | Dataclasses, shared mutable state, copies, invariants, inheritance, `super`, polymorphism, `Protocol`, state transitions, duplicate events, refunds |
| 21–30 | APIs and clients | Routing, response status, validation, PUT/PATCH, idempotency, pagination, retries, deadlines, rate limits, ETags, guarded page fetching |
| 31–40 | SQL and transactions | Parameterized queries, joins, NULL, aggregation, unique constraints, window functions, rollback, version conflicts, savepoints, transactional outbox |
| 41–50 | System components | TTL, LRU, message delivery, visibility timeouts, circuit breakers, dependencies, consistent hashing, replica reads, reservations, payment integration |

Useful standard libraries appear where you need them: `decimal`, `collections`,
`csv`, `json`, `typing`, `datetime`, `itertools`, `heapq`, `dataclasses`, `copy`,
`sqlite3`, and `bisect`. No package installation is needed in the editor.

The SQL reference solutions use a real in-memory SQLite database. API and
distributed-system problems use deterministic request and event sequences.
They teach component behavior without requiring a running server or network.
They do not test real parallel execution, deployment, or operating a database.

The judge checks results. It cannot prove that you used inheritance, type
annotations, SQL, or a particular complexity. Use the technique requested by
the lesson. A separate code review can check those choices. The course does
not cover every technical interview topic.

## Files and checks

- `authoring/pNN.py`: lesson, contract, independent Python and Java solutions,
  explicit expected cases, additional inputs, and a realistic faulty mutation.
- `problems/c1-*`: generated native CoJudge content. The starter contains no
  completed reference answer, except intentional bug-fix tasks.
- `courses/capital-one-engineering-50`: the ordered course index.
- `instructor/`: reference files and labeled case expectations for verification.
  These files never go into learner attempts or the site's problem directory.

From the repository root:

```bash
uv run python scripts/verify_cojudge.py
uv run python scripts/build_cojudge.py
uv run pytest -q tests/test_cojudge.py
```

Use `--only 1 2 3` while editing a small group. The local verifier compares both
implementations against explicit expectations. It compares additional cases
across the two implementations. It also checks reversed execution order,
rejects realistic faulty implementations, and tests wrong output types.
Generated expected values alone are not independent evidence.
The verifier also runs 51 separate cases from the independent review. Their
expected results come from the contracts and direct arithmetic. See
[the review record](review.md) for the findings and corrections.

Live verification uses the existing site's Run and Submit endpoints. It does
not write browser completion marks or learner solutions. The script accepts an
authorized local SSH tunnel:

```bash
uv run python scripts/check_cojudge_live.py \
  --base-url http://127.0.0.1:15378 --include-review \
  --report /tmp/cojudge-live.json
```

Use the local port of the authorized tunnel for the current deployment.
The script submits every prepared faulty variant. A wrong answer must reject
each variant; a runner failure does not count. `--include-review` also checks
both the reference output and the judge answer against the manual expectations
for the 51 review cases.

Publish only `problems/` and `courses/` to the CoJudge content directory.
Keep the new course index unpublished until all its problems pass live checks.
Do not replace other course files or copy `instructor/` into learner folders.
