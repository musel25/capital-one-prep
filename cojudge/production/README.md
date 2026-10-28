# Software Engineering Tickets

[Open the course](https://cojudge.musel.dev/?course=software-engineering).

24 independent Python tickets use a short input/output contract. Each ticket has
three examples, explicit input limits, submission tests, and an optional reference
solution. There are no lessons or extra practice instructions in the statements.

| Tickets | Programming work |
| --- | --- |
| 01–06 | Email cleanup, configuration flags, request validation, service logs, cursor pagination, settings patches |
| 07–10 | Log redaction, bounded retries, page collection, idempotent jobs |
| 11–14 | Cache expiry, rate limits, versioned events, stock reservations |
| 15–16 | Job visibility and atomic transfers |
| 17–20 | CSV, UTC dates, access permissions, relative paths |
| 21–24 | Semantic versions, build dependencies, record synchronization, HTML escaping |

Implement the named function at the top of the editor. The supplied adapter reads
the judge input, calls the function, checks that input objects were not changed,
and serializes the result. Each call starts with fresh state. Custom cases use the
same JSON object as the examples in the `payload` field.

The course tests programming behavior in a deterministic process. It does not run
concurrent workers or deploy services. The transfer reference uses real in-memory
SQLite transactions. The CSV and timestamp references use standard libraries.
The output judge does not require a particular implementation technique.

## Authoring and verification

`tickets/pNN.py` contains the contract, manually expected cases, named Python
function, independent Java marker, and plausible faults. Each fault must compile
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
