# 03. Reading Data with Select

[Course list](/?course=pybites-sqlmodel) · [Original bite](https://pybitesplatform.com/bites/reading-data-with-select/)

Implement `get_workouts(session)` in ID order, `get_workout(session, workout_id)`
returning a row or `None`, and `find_exercises(session, muscle_group=None)` in ID order.
A group filter uses exact, case-sensitive equality. `None` means all groups. An empty
string selects the empty group. Reads must not insert or change rows.

**Source:** The original template and tests require Pybites premium. This version
uses a recreated template and tests based on the public description.

<details>
<summary>Original public description</summary>

Now that you can insert workouts and exercises, the gym staff needs to retrieve them. Time to learn how to query your database!
In SQLModel, you build queries using the select() function. Think of it like asking the database a question: "Give me all workouts" or "Find the exercise named 'Squats'".

</details>

Write your code above the supplied tests. Use Python 3.11 with the supplied SQLModel,
SQLAlchemy, Pydantic, FastAPI, HTTPX, and pytest packages. Tests use SQLite without
network access. Each test gets a separate database.

**Run** checks the first three tests. **Submit** checks all 6 tests. A failure
shows the pytest error. The runner executes the suite once and returns each test's
result. Keep the supplied tests and runner. The reference solution button contains
the implementation to paste above them.
