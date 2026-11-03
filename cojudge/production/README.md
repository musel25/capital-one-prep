# Software Engineering Tickets

[Open the course](https://cojudge.musel.dev/?course=software-engineering).

15 independent Python tickets from real services. Each ticket has four parts:

- **The ticket** and **Why it matters**: the situation and what goes wrong in production.
- **Your task**: numbered rules, one rule per line, and short constraints.
- A step-by-step starter with TODO comments, plus three hints (concept, then mechanics, then detail).
- An explained solution: how it works, common mistakes, and the reference code.

| Stage | Tickets |
| --- | --- |
| 01 Clean input | Email cleanup, configuration flags, request validation |
| 02 Data and APIs | Cursor pagination, settings patches, UTC dates, log redaction |
| 03 Reliability | Bounded retries, idempotent jobs, cache expiry, versioned events |
| 04 Security and money | Access rules, HTML escaping, upload paths, atomic transfers |

Display numbers are 01–15. Problem IDs keep their original `pe-NN` numbers, so
saved work and URLs stay valid. Nine tickets are retired from the course index
because they repeat another ticket or a Pybites exercise, or are specialized:
04, 09, 12, 14, 15, 17, 21, 22, 23. Their files stay in `tickets/` and `problems/`.

Implement the named function at the top of the editor. The supplied adapter reads
the judge input, calls the function, checks that input objects were not changed,
and serializes the result. Each call starts with fresh state.

## Authoring and verification

`tickets/pNN.py` contains the contract, manually expected cases, named Python
function, independent Java marker, and plausible faults. `guide.py` holds the
course order, the learner text, the starters, the hints, and the explanations.
Verification also checks that each starter fails at least one case, and that the
simple transfer solution passes every case. Each fault must compile
and fail at least one case. Python checks also run cases in reverse order and
check input preservation. Java checks reject incorrect output types and malformed
JSON. Cases never derive their expected values from the implementation.

```bash
uv run python scripts/production_course.py verify
uv run python scripts/production_course.py build
uv run pytest -q
uv run python scripts/production_course.py live --base-url http://127.0.0.1:15379
```

`live` uses the existing site's Submit API through an authorized SSH tunnel. It
does not write browser solutions or completion flags. Publish problem files first.
Publish `courses/software-engineering/courseinfo.json` after live checks pass.

The live lists `capital-one-codebase-practice`, `capital-one-engineering-50`, and
`python-oop` are retired. Their authoring files and old generated indexes remain
in the repository for history. Do not republish those indexes when you publish
this course. Learner solutions and old problem URLs remain available.
