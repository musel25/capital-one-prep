# 04. Update and Delete Operations

[Course list](/?course=pybites-sqlmodel) · [Original bite](https://pybitesplatform.com/bites/update-and-delete-operations/)

Implement `update_workout(session, workout_id, **changes)`. Only `name` and
`description` can change. Reject every unknown field with `ValueError` before any
change. Return `None` for a missing row. An empty update returns the existing row.
Commit and refresh successful updates. Implement `delete_workout(session, workout_id)`.
Commit a deletion and return `True`. Return `False` if the row is missing. Preserve other rows.

**Source:** The original template and tests require Pybites premium. This version
uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

The gym needs to fix typos in workout names and remove discontinued programs. Time to complete your CRUD (Create, Read, Update, Delete) skills!
SQLModel makes updates simple: fetch the object, modify it, commit. No special UPDATE statements needed!

</details>

Write your code above the supplied tests. Use Python 3.11 with the supplied SQLModel,
SQLAlchemy, Pydantic, FastAPI, HTTPX, and pytest packages. Tests use SQLite without
network access. Each test gets a separate database.

**Run** checks the first three tests. **Submit** checks all 6 tests. A failure
shows the pytest error. The runner executes the suite once and returns each test's
result. Keep the supplied tests and runner. The reference solution button contains
the implementation to paste above them.
