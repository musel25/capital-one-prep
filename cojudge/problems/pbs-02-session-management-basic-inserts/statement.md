# 02. Session Management & Basic Inserts

[Course list](/?course=pybites-sqlmodel) · [Original bite](https://pybitesplatform.com/bites/session-management-basic-inserts/)

The two table models are supplied. Implement `add_workout(session, name, description="")`
and `add_exercise(session, name, muscle_group="")`. Add one row, commit, refresh, and
return that model with its database ID. Do not close the caller's session. Repeated
names are allowed. Implement `get_session(engine)` as a generator that yields a
Session inside a context manager. An uncommitted insert must roll back when it closes.

**Source:** The original template and tests require Pybites premium. This version
uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Great job creating your database tables! Now the gym owner wants to start adding workout programs to the database.
In this exercise, you'll learn how to safely insert data into your database using SQLModel's Session object.

</details>

Write your code above the supplied tests. Use Python 3.11 with the supplied SQLModel,
SQLAlchemy, Pydantic, FastAPI, HTTPX, and pytest packages. Tests use SQLite without
network access. Each test gets a separate database.

**Run** checks the first three tests. **Submit** checks all 6 tests. A failure
shows the pytest error. The runner executes the suite once and returns each test's
result. Keep the supplied tests and runner. The reference solution button contains
the implementation to paste above them.
